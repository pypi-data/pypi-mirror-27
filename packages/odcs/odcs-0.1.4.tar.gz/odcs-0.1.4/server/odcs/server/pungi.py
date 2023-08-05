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

import os
import shutil
import tempfile
import jinja2

import odcs.server.utils
from odcs.server import conf, log
from odcs.server import comps
from odcs.common.types import PungiSourceType, COMPOSE_RESULTS


class PungiConfig(object):
    def __init__(self, release_name, release_version, source_type, source,
                 packages=None, arches=None, sigkeys=None, results=0):
        self.release_name = release_name
        self.release_version = release_version
        self.bootable = False
        self.sigkeys = sigkeys.split(" ") if sigkeys else []
        self.pdc_url = conf.pdc_url
        self.pdc_insecure = conf.pdc_insecure
        self.pdc_develop = conf.pdc_develop
        self.source_type = source_type
        self.source = source
        self.koji_profile = conf.koji_profile
        self.pkgset_koji_inherit = True
        if arches:
            self.arches = arches
        else:
            self.arches = conf.arches
        self.packages = packages or []

        # Store results as list of strings, so it can be used by jinja2
        # templates.
        self.results = []
        for k, v in COMPOSE_RESULTS.items():
            if results & v:
                self.results.append(k)

        if source_type == PungiSourceType.KOJI_TAG:
            self.koji_tag = source
            self.gather_source = "comps"
            self.gather_method = "deps"
        elif source_type == PungiSourceType.MODULE:
            # We have to set koji_tag to something even when we are not using
            # it.
            self.koji_tag = None
            self.gather_source = "module"
            self.gather_method = "nodeps"

            if self.packages:
                raise ValueError("Exact packages cannot be set for MODULE "
                                 "source type.")
        elif source_type == PungiSourceType.REPO:
            self.gather_source = "comps"
            self.gather_method = "deps"
            self.koji_tag = None
        else:
            raise ValueError("Unknown source_type %r" % source_type)

    @property
    def release_short(self):
        return self.release_name[:16]

    @property
    def comps_file(self):
        if self.source_type == PungiSourceType.MODULE:
            return None
        else:
            return "comps.xml"

    @property
    def pkgset_source(self):
        if self.source_type == PungiSourceType.REPO:
            return 'repos'
        return 'koji'

    def get_comps_config(self):
        if self.source_type == PungiSourceType.MODULE:
            return ""
        odcs_comps = comps.Comps()
        odcs_group = comps.Group('odcs-group', 'odcs-group', 'ODCS compose default group')
        for package in self.packages:
            odcs_group.add_package(comps.Package(package))
        odcs_comps.add_group(odcs_group)

        template = jinja2.Template(comps.COMPS_TEMPLATE)
        return template.render(comps=odcs_comps)

    def get_variants_config(self):
        odcs_product = comps.Product()
        tmp_variant = comps.Variant('Temporary', 'Temporary', 'variant', self.source_type)
        for arch in self.arches:
            tmp_variant.add_arch(comps.Arch(arch))
        if self.source_type == PungiSourceType.MODULE:
            for module in self.source.split(" "):
                tmp_variant.add_module(comps.Module(module))
        elif self.source_type == PungiSourceType.KOJI_TAG:
            if self.packages:
                tmp_variant.add_group(comps.Group('odcs-group', 'odcs-group', 'ODCS compose default group'))

        odcs_product.add_variant(tmp_variant)

        template = jinja2.Template(comps.VARIANTS_TEMPLATE)
        return template.render(product=odcs_product)

    def get_pungi_config(self):
        try:
            with open(conf.pungi_conf_path) as fd:
                template = jinja2.Template(fd.read())
            return template.render(config=self)
        except Exception as e:
            log.exception(
                "Failed to render pungi conf template {!r}: {}".format(conf.pungi_conf_path,
                                                                       str(e)))


class Pungi(object):
    def __init__(self, pungi_cfg, koji_event=None):
        self.pungi_cfg = pungi_cfg
        self.koji_event = koji_event

    def _write_cfg(self, fn, cfg):
        with open(fn, "w") as f:
            log.info("Writing %s configuration to %s.", os.path.basename(fn), fn)
            f.write(cfg)

    def run(self):
        td = None
        try:
            td = tempfile.mkdtemp()

            main_cfg = self.pungi_cfg.get_pungi_config()
            variants_cfg = self.pungi_cfg.get_variants_config()
            comps_cfg = self.pungi_cfg.get_comps_config()
            log.debug("Main Pungi config:")
            log.debug("%s", main_cfg)
            log.debug("Variants.xml:")
            log.debug("%s", variants_cfg)
            log.debug("Comps.xml:")
            log.debug("%s", comps_cfg)

            self._write_cfg(os.path.join(td, "pungi.conf"), main_cfg)
            self._write_cfg(os.path.join(td, "variants.xml"), variants_cfg)
            self._write_cfg(os.path.join(td, "comps.xml"), comps_cfg)

            pungi_cmd = [
                conf.pungi_koji, "--config=%s" % os.path.join(td, "pungi.conf"),
                "--target-dir=%s" % conf.target_dir, "--nightly"]

            if self.koji_event:
                pungi_cmd += ["--koji-event", str(self.koji_event)]

            odcs.server.utils.execute_cmd(pungi_cmd, cwd=td)
        finally:
            try:
                if td is not None:
                    shutil.rmtree(td)
            except Exception as e:
                log.warning(
                    "Failed to remove temporary directory {!r}: {}".format(
                        td, str(e)))
