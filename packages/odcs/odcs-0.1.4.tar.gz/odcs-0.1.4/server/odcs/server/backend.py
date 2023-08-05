# -*- coding: utf-8 -*-
# Copyright (c) 2017  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Jan Kaluza <jkaluza@redhat.com>

import koji
import os
import threading
import shutil
import six
import productmd.compose
import productmd.common
from datetime import datetime
from odcs.server import log, conf, app, db
from odcs.server.models import Compose, COMPOSE_STATES, COMPOSE_FLAGS
from odcs.server.pungi import Pungi, PungiConfig, PungiSourceType
from odcs.server.pulp import Pulp
from concurrent.futures import ThreadPoolExecutor
import glob
import odcs.server.utils
import odcs.server.pdc
import defusedxml.ElementTree


class BackendThread(object):
    """
    Base BackendThread class.

    The `BackendThread.do_work(...)` is called repeatedly after `timeout`
    seconds.
    """
    def __init__(self, timeout=1):
        """
        Creates new BackendThread instance.

        :param int timeout: Timeout in seconds after which do_work is called.
        """
        self.thread = None
        self.exit = False
        self.exit_cond = threading.Condition()
        self.timeout = timeout

    def do_work(self):
        """
        Reimplement this method in your own BackendThread subclass.
        This method is called every `timeout` seconds.
        """
        raise NotImplemented("do_work() method not implemented")

    def _run(self):
        """
        Main "run" method of a thread. Calls `do_work()` after `self.timeout`
        seconds. Stops then `stop()` is called.
        """
        while not self.exit:
            try:
                self.do_work()
            except Exception:
                log.exception("Exception in backend thread")
            self.exit_cond.acquire()
            self.exit_cond.wait(float(self.timeout))
            self.exit_cond.release()

    def join(self):
        """
        Waits until the thread terminates.
        """
        self.thread.join()

    def stop(self):
        """
        Stops the thread.
        """
        self.exit = True
        self.exit_cond.acquire()
        self.exit_cond.notify()
        self.exit_cond.release()

    def start(self):
        """
        Starts the thread.
        """
        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()


class RemoveExpiredComposesThread(BackendThread):
    """
    Thread used to remove old expired composes.
    """
    def __init__(self):
        """
        Creates new RemoveExpiredComposesThread instance.
        """
        super(RemoveExpiredComposesThread, self).__init__(10)

    def _remove_compose_dir(self, toplevel_dir):
        """
        Removes the compose toplevel_dir symlink together with the real
        path it points to.
        """

        # Be nice and don't fail when directory does not exist.
        if not os.path.exists(toplevel_dir):
            log.warn("Cannot remove directory %s, it does not exist",
                     toplevel_dir)
            return

        # If toplevel_dir is a symlink, remove the symlink and
        # its target. If toplevel_dir is normal directory, just
        # remove it using rmtree.
        if os.path.realpath(toplevel_dir) != toplevel_dir:
            targetpath = os.path.realpath(toplevel_dir)
            os.unlink(toplevel_dir)
            if os.path.exists(targetpath):
                shutil.rmtree(targetpath)
        else:
            shutil.rmtree(toplevel_dir)

    def _get_compose_id_from_path(self, path):
        """
        Returns the ID of compose from directory path in conf.target_dir.
        """
        parts = os.path.basename(path).split("-")
        while parts and parts[0] != "odcs":
            del parts[0]

        if not parts or len(parts) < 2 or not parts[1].isdigit():
            log.error("Directory %s is not valid compose directory", path)
            return None

        return int(parts[1])

    def do_work(self):
        """
        Checks for the expired composes and removes them.
        """
        log.info("Checking for expired composes")

        composes = Compose.composes_to_expire()
        for compose in composes:
            log.info("%r: Removing compose", compose)
            compose.state = COMPOSE_STATES["removed"]
            compose.time_removed = datetime.utcnow()
            db.session.commit()
            if not compose.reused_id:
                self._remove_compose_dir(compose.toplevel_dir)

        # In case of ODCS error, there might be left-over directories
        # belonging to already expired composes. Try to find them in the
        # target_dir.
        # At first, get all the directories in target_dir which are created
        # by ODCS.
        odcs_paths = []
        for dirname in ["latest-odcs-*", "odcs-*"]:
            path = os.path.join(conf.target_dir, dirname)
            odcs_paths += glob.glob(path)

        # Then try removing them if they are left there by some error.
        for path in odcs_paths:
            # Check that we are really going to remove a directory.
            if not os.path.isdir(path):
                continue

            compose_id = self._get_compose_id_from_path(path)
            if not compose_id:
                # Error logged in _get_compose_id_from_dirname already.
                continue

            composes = Compose.query.filter(Compose.id == compose_id).all()
            if not composes:
                log.info("Removing data of compose %d - it is not in "
                         "database: %s", compose_id, path)
                self._remove_compose_dir(path)
                continue

            compose = composes[0]
            if compose.state == COMPOSE_STATES["removed"]:
                log.info("%r: Removing data of compose - it has already "
                         "expired some time ago: %s", compose_id, path)
                self._remove_compose_dir(path)
                continue


def create_koji_session():
    """
    Creates and returns new koji_session based on the `conf.koji_profile`.
    """

    koji_module = koji.get_profile_module(conf.koji_profile)
    session_opts = {}
    for key in ('krbservice', 'timeout', 'keepalive',
                'max_retries', 'retry_interval', 'anon_retry',
                'offline_retry', 'offline_retry_interval',
                'debug', 'debug_xmlrpc', 'krb_rdns',
                'use_fast_upload'):
        value = getattr(koji_module.config, key, None)
        if value is not None:
            session_opts[key] = value
    koji_session = koji.ClientSession(koji_module.config.server,
                                      session_opts)
    return koji_session


def koji_get_inherited_tags(koji_session, tag, tags=None):
    """
    Returns list of ids of all tags the tag `tag` inherits from.
    """

    info = koji_session.getTag(tag)
    ids = [info["id"]]
    seen_tags = tags or set()
    inheritance_data = koji_session.getInheritanceData(tag)
    inheritance_data = [data for data in inheritance_data
                        if data['parent_id'] not in seen_tags]

    # Iterate over all the tags this tag inherits from.
    for inherited in inheritance_data:
        # Make a note to ourselves that we have seen this parent_tag.
        parent_tag_id = inherited['parent_id']
        seen_tags.add(parent_tag_id)

        # Get tag info for the parent_tag.
        info = koji_session.getTag(parent_tag_id)
        if info is None:
            log.error("Cannot get info about Koji tag %s", parent_tag_id)
            return []

        ids += koji_get_inherited_tags(koji_session, info['name'], seen_tags)

    return ids


def resolve_compose(compose):
    """
    Resolves various general compose values to the real ones. For example:
    - Sets the koji_event based on the current Koji event, so it can be used
      to generate the compose and we can find out if we can reuse that compose
      later
    - For MODULE PungiSourceType, resolves the modules without the "release"
      field to latest module release using PDC.
    """
    if compose.source_type == PungiSourceType.REPO:
        # We treat "revision" of local repo as koji_event for the simplicity.
        repomd = os.path.join(compose.source, "repodata", "repomd.xml")
        e = defusedxml.ElementTree.parse(repomd).getroot()
        revision = e.find("{http://linux.duke.edu/metadata/repo}revision").text
        compose.koji_event = int(revision)
    elif compose.source_type == PungiSourceType.KOJI_TAG:
        # If compose.koji_event is set, it means that we are regenerating
        # previous compose and we have to respect the previous koji_event to
        # get the same results.
        if not compose.koji_event:
            koji_session = create_koji_session()
            compose.koji_event = int(koji_session.getLastEvent()['id'])
    elif compose.source_type == PungiSourceType.MODULE:
        # Resolve the latest release of modules which do not have the release
        # string defined in the compose.source.
        pdc = odcs.server.pdc.PDC(conf)
        modules = compose.source.split(" ")

        specified_modules = []
        for module in modules:
            variant_dict = pdc.variant_dict_from_str(module)
            specified_modules.append(pdc.get_latest_module(**variant_dict))

        expand = not compose.flags & COMPOSE_FLAGS["no_deps"]
        new_modules = pdc.validate_module_list(specified_modules, expand=expand)

        uids = sorted(m["variant_uid"] for m in new_modules)
        compose.source = ' '.join(uids)


def get_reusable_compose(compose):
    """
    Returns the compose in the "done" state which contains the same artifacts
    and results as the compose `compose` and therefore could be reused instead
    of generating new one.
    """

    # Get all the active composes of the same source_type
    composes = db.session.query(Compose).filter(
        Compose.state == COMPOSE_STATES["done"],
        Compose.source_type == compose.source_type).all()

    for old_compose in composes:
        # Skip the old_compose in case it reuses another compose. In that case
        # the reused compose is also in composes list, so we won't miss it. We
        # don't want chain of composes reusing each other, because it would
        # break the time_to_expire handling.
        if old_compose.reused_id:
            continue

        packages = set(compose.packages.split(" ")) \
            if compose.packages else set()
        old_packages = set(old_compose.packages.split(" ")) \
            if old_compose.packages else set()
        if packages != old_packages:
            log.debug("%r: Cannot reuse %r - packages not same", compose,
                      old_compose)
            continue

        source = set(compose.source.split(" "))
        old_source = set(old_compose.source.split(" "))
        if source != old_source:
            log.debug("%r: Cannot reuse %r - sources not same", compose,
                      old_compose)
            continue

        if compose.flags != old_compose.flags:
            log.debug("%r: Cannot reuse %r - flags not same, %d != %d",
                      compose, old_compose, compose.flags,
                      old_compose.flags)
            continue

        if compose.results != old_compose.results:
            log.debug("%r: Cannot reuse %r - results not same, %d != %d",
                      compose, old_compose, compose.results,
                      old_compose.results)
            continue

        sigkeys = set(compose.sigkeys.split(" ")) \
            if compose.sigkeys else set()
        old_sigkeys = set(old_compose.sigkeys.split(" ")) \
            if old_compose.sigkeys else set()
        if sigkeys != old_sigkeys:
            log.debug("%r: Cannot reuse %r - sigkeys not same", compose,
                      old_compose)
            continue

        if compose.source_type == PungiSourceType.KOJI_TAG:
            # For KOJI_TAG compose, check that all the inherited tags by our
            # Koji tag have not changed since previous old_compose.
            koji_session = create_koji_session()
            tags = koji_get_inherited_tags(koji_session, compose.source)
            if not tags:
                continue
            changed = koji_session.tagChangedSinceEvent(
                old_compose.koji_event, tags)
            if changed:
                log.debug("%r: Cannot reuse %r - one of the tags changed "
                          "since previous compose: %r", compose, old_compose,
                          tags)
                continue
        elif compose.koji_event != old_compose.koji_event:
            log.debug("%r: Cannot reuse %r - koji_events not same, %d != %d",
                      compose, old_compose, compose.koji_event,
                      old_compose.koji_event)
            continue

        return old_compose

    return None


def reuse_compose(compose, compose_to_reuse):
    """
    Changes the attribute of `compose` in a way it reuses
    the `compose_to_reuse`.
    """

    # Set the reuse_id
    compose.reused_id = compose_to_reuse.id
    # Set the time_to_expire to bigger value from both composes.
    compose.time_to_expire = max(compose.time_to_expire,
                                 compose_to_reuse.time_to_expire)
    compose_to_reuse.time_to_expire = compose.time_to_expire


def _write_repo_file(compose, data=None):
    """
    Writes main repo file for a resulting compose containing the `data`.
    If `data` is not provided, the default one pointing to pungi compose
    will be generated.
    """
    if not data:
        baseurl = os.path.join(
            compose.result_repo_url, "$basearch", "os")
        data = """[%s]
name=ODCS repository for compose %s
baseurl=%s
type=rpm-md
skip_if_unavailable=False
gpgcheck=0
repo_gpgcheck=0
enabled=1
enabled_metadata=1
""" % (compose.name, compose.name, baseurl)

    # Ensure the directory exists
    dirname = os.path.dirname(compose.result_repofile_path)
    odcs.server.utils.makedirs(dirname)

    with open(compose.result_repofile_path, "w") as f:
        f.write(data)


def generate_pulp_compose(compose):
    """
    Generates the compose of PULP type - this basically means only
    repo file pointing to data in pulp.
    """
    content_sets = compose.source.split(" ")

    pulp = Pulp(server_url=conf.pulp_server_url,
                username=conf.pulp_username,
                password=conf.pulp_password)

    repofile = ""

    for arch in conf.arches:
        repos = pulp.get_repo_urls_from_content_sets(content_sets, arch)

        if len(repos) != len(content_sets):
            err = "Failed to find all the content_sets %r in the Pulp, " \
                "found only %r" % (content_sets, repos.keys())
            log.error(err)
            raise ValueError(err)

        for name in sorted(repos.keys()):
            url = repos[name]
            r = """
[%s]
name=%s
baseurl=%s
enabled=1
gpgcheck=0
""" % (name, name, url)
            repofile += r

    _write_repo_file(compose, repofile)

    compose.state = COMPOSE_STATES["done"]
    log.info("%r: Compose done", compose)
    compose.time_done = datetime.utcnow()
    db.session.add(compose)
    db.session.commit()


def generate_pungi_compose(compose):
    """
    Generates the compose of KOJI, TAG, or REPO type using the Pungi tool.
    """
    # Reformat the data from database
    packages = compose.packages
    if packages:
        packages = packages.split(" ")

    # Resolve the general data in the compose.
    resolve_compose(compose)

    # Check if we can reuse some existing compose instead of
    # generating new one.
    compose_to_reuse = get_reusable_compose(compose)
    if compose_to_reuse:
        log.info("%r: Reusing compose %r", compose, compose_to_reuse)
        reuse_compose(compose, compose_to_reuse)
    else:
        # Generate PungiConfig and run Pungi
        pungi_cfg = PungiConfig(compose.name, "1", compose.source_type,
                                compose.source, packages=packages,
                                sigkeys=compose.sigkeys,
                                results=compose.results)
        if compose.flags & COMPOSE_FLAGS["no_deps"]:
            pungi_cfg.gather_method = "nodeps"
        if compose.flags & COMPOSE_FLAGS["no_inheritance"]:
            pungi_cfg.pkgset_koji_inherit = False

        koji_event = None
        if compose.source_type == PungiSourceType.KOJI_TAG:
            koji_event = compose.koji_event

        pungi = Pungi(pungi_cfg, koji_event)
        pungi.run()

        _write_repo_file(compose)

    # If there is no exception generated by the pungi.run(), we know
    # the compose has been successfully generated.
    compose.state = COMPOSE_STATES["done"]
    log.info("%r: Compose done", compose)
    compose.time_done = datetime.utcnow()
    db.session.add(compose)
    db.session.commit()


def validate_pungi_compose(compose):
    """
    Validate the compose is generated by pungi as expected.
    """
    # the requested packages should be present in the generated compose
    if compose.packages:
        packages = compose.packages.split()
        pungi_compose = productmd.compose.Compose(compose.toplevel_dir)
        rm = pungi_compose.rpms.rpms
        srpm_nevras = []
        for variant in rm:
            for arch in rm[variant]:
                for srpm_nevra, data in six.iteritems(rm[variant][arch]):
                    for rpm_nevra, data in six.iteritems(rm[variant][arch][srpm_nevra]):
                        if data['category'] != 'source':
                            continue
                        srpm_nevras.append(srpm_nevra)
        srpms = [productmd.common.parse_nvra(n)['name'] for n in srpm_nevras]
        not_found = []
        for pkg in packages:
            if pkg not in srpms:
                not_found.append(pkg)
        if not_found:
            msg = "The following requested packages are not present in the generated compose: %s." % \
                  " ".join(not_found)
            log.error(msg)
            raise RuntimeError(msg)


def generate_compose(compose_id):
    """
    Generates the compose defined by its `compose_id`. It is run by
    ThreadPoolExecutor from the ComposerThread.
    """
    compose = None
    with app.app_context():
        try:
            # Get the compose from database.
            compose = Compose.query.filter(Compose.id == compose_id).one()
            log.info("%r: Starting compose generation", compose)

            if compose.source_type == PungiSourceType.PULP:
                # Pulp compose is special compose not generated by Pungi.
                # The ODCS in this case just creates .repo file which points
                # to composes generated by pulp/pub.
                generate_pulp_compose(compose)
            else:
                generate_pungi_compose(compose)
                validate_pungi_compose(compose)
        except Exception:
            # Something went wrong, log the exception and update the compose
            # state in database.
            if compose:
                log.exception("%r: Error while generating compose", compose)
            else:
                log.exception("Error while generating compose %d", compose_id)
            compose.state = COMPOSE_STATES["failed"]
            compose.time_done = datetime.utcnow()
            db.session.add(compose)
            db.session.commit()

    # consolidate duplicate files in compose target dir
    if compose and compose.reused_id is None and compose.source_type != PungiSourceType.PULP:
        try:
            log.info("Running hardlink to consolidate duplicate files in compose target dir")
            odcs.server.utils.hardlink(conf.target_dir)
        except Exception as ex:
            # not fail, just show warning message
            log.warn("Error while running hardlink on system: %s" % ex.message, exc_info=True)


class ComposerThread(BackendThread):
    """
    Thread used to query the database for composes in "wait" state and
    generating the composes using Pungi.
    """
    def __init__(self):
        """
        Creates new ComposerThread instance.
        """
        super(ComposerThread, self).__init__(1)
        self.executor = ThreadPoolExecutor(conf.num_concurrent_pungi)

    def do_work(self):
        """
        Gets all the composes in "wait" state. Generates them using Pungi
        by calling `generate_compose(...)` in ThreadPoolExecutor.
        """
        composes = Compose.query.filter(
            Compose.state == COMPOSE_STATES["wait"]).all()

        for compose in composes:
            log.info("%r: Going to start compose generation.", compose)
            compose.state = COMPOSE_STATES["generating"]
            db.session.add(compose)
            db.session.commit()
            self.executor.submit(generate_compose, compose.id)


def run_backend():
    """
    Runs the backend.
    """
    while True:
        remove_expired_composes_thread = RemoveExpiredComposesThread()
        composer_thread = ComposerThread()
        try:
            remove_expired_composes_thread.start()
            composer_thread.start()
            remove_expired_composes_thread.join()
            composer_thread.join()
        except KeyboardInterrupt:
            remove_expired_composes_thread.stop()
            composer_thread.stop()
            remove_expired_composes_thread.join()
            composer_thread.join()
            return 0
        except Exception:
            log.exception("Exception in backend")
            remove_expired_composes_thread.stop()
            composer_thread.stop()
            remove_expired_composes_thread.join()
            composer_thread.join()

    return 0
