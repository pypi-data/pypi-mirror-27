# Copyright (c) 2017, Kevin Lopez <kevin@kevlopez.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.
# pylint: disable=missing-docstring

import sys
import os
import json
import shutil
import argparse
import subprocess
import shlex


class FlatpakDev:

    def __init__(self):
        self.flatpak_dev_dir = os.path.expanduser("~/.config/FlatpakDev/")
        self.dict_path = os.path.join(self.flatpak_dev_dir, "Dict.json")
        self.manifests_dir = os.path.join(self.flatpak_dev_dir,
                                          "FlatpakManifests/")
        self.builds_dir = os.path.join(self.flatpak_dev_dir, "Builds/")
        self.flatpak_builds_dir = os.path.join(self.flatpak_dev_dir,
                                               "FlatpakBuilds/")

    def create_json_dict(self):
        if not os.path.exists(self.dict_path):
            if not os.path.exists(self.flatpak_dev_dir):
                os.mkdir(self.flatpak_dev_dir, mode=0o755)
            with open(self.dict_path, mode="x") as json_file:
                json_dict = {}
                json.dump(json_dict, json_file)

    def create_manifests_directory(self):
        if not os.path.exists(self.manifests_dir):
            os.mkdir(self.manifests_dir)

    def create_builds_directory(self):
        if not os.path.exists(self.builds_dir):
            os.mkdir(self.builds_dir)

    def create_flatpak_builds_directory(self):
        if not os.path.exists(self.flatpak_builds_dir):
            os.mkdir(self.flatpak_builds_dir)

    def list_apps(self):
        with open(self.dict_path, mode="r") as json_file:
            data = json.load(json_file)
            for app in data:
                print(app)

    def install(self, source_dir, manifest, name=None):
        self.create_json_dict()
        self.create_manifests_directory()
        self.create_builds_directory()
        self.create_flatpak_builds_directory()

        source_dir = os.path.abspath(source_dir)
        if name is None:
            name = os.path.basename(source_dir)

        app = FlatpakApp(source_dir,
                         name,
                         manifest,
                         self.builds_dir,
                         self.flatpak_builds_dir,
                         self.manifests_dir,
                         self.flatpak_dev_dir)

        app.create_modified_manifest(self.manifests_dir,
                                     self.flatpak_dev_dir)

        with open(self.dict_path, mode="r+") as json_file:
            data = json.load(json_file)
            data[app.name] = {
                    "source-dir": app.source_dir,
                    "manifest": app.modified_manifest,
                    "build-dir": app.build_dir,
                    "flatpak-build-dir": app.flatpak_build_dir,
                    "finish-args": app.finish_args,
                    "configure-command": app.configure_command,
                    "make-command": app.make_command,
                    "make-install-command": app.make_install_command
            }
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

        app.build_flatpak_module()
        app.run_configure()
        app.run_make()
        app.run_make_install()

        self.enter_sandbox(app.name)

    def enter_sandbox(self, name):
        with open(self.dict_path, mode="r") as json_file:
            data = json.load(json_file)
            app = data[name]
            message = "Welcome to the Sandbox"
            echo = "echo -e \"{}\"".format(message)
            commands = "cd {};{};{};{}".format(app["source-dir"], "tput clear", echo, "bash")
            bash_script = "bash -c '{}'".format(commands)
            command = ["flatpak-builder", "--run"] + app["finish-args"] + \
                      [app["flatpak-build-dir"], app["manifest"]] + \
                      shlex.split(bash_script)

            subprocess.run(command, cwd=self.flatpak_dev_dir, check=True)

    def make_and_install(self, name):
        with open(self.dict_path, mode="r") as json_file:
            data = json.load(json_file)
            app = data[name]
            subprocess.run(app["make-command"], cwd=app["build-dir"], check=True)
            subprocess.run(app["make-install-command"], cwd=app["build-dir"], check=True)


class FlatpakApp:

    def __init__(self, source_dir, name, manifest, builds_dir,
                 flatpak_builds_dir, manifests_dir, cwd):
        self.name = name
        self.id = None
        self.source_dir = os.path.abspath(source_dir)
        self.build_dir = os.path.join(builds_dir,
                                      "{}-{}".format(self.name, "build"))
        self.flatpak_build_dir = os.path.join(flatpak_builds_dir,
                                              "{}-{}".format(self.name,
                                                             "build"))
        self.manifest = None
        self.manifest_name = None
        self.modified_manifest = None
        self.module_name = None
        self.module = None
        self.configure_command = None
        self.make_command = None
        self.make_install_command = None
        self.finish_args = None
        self.cwd = cwd

        self.parse_manifest(manifest)
        self.create_modified_manifest(manifests_dir, cwd)

    def parse_manifest(self, manifest):
        with open(manifest) as json_file:
            data = json.load(json_file)
            auxModule = data["modules"][-1]
            self.module_name = auxModule["name"]
            self.finish_args = data["finish-args"]
            self.manifest = json_file.name
            self.manifest_name = os.path.basename(self.manifest)


            aux = self.module = FlatpakModule(auxModule)
            self.configure_command = aux.get_configure_command(self.source_dir,
                                                               self.build_dir)
            self.make_command = aux.get_make_command(self.build_dir)
            self.make_install_command = aux.get_make_install_command(self.build_dir)


    def create_modified_manifest(self, manifests_dir, flatpak_dev_dir):
        self.modified_manifest = os.path.join(manifests_dir,
                                              self.manifest_name)
        shutil.copyfile(self.manifest, self.modified_manifest)

        with open(self.modified_manifest, mode="r+") as json_file:
            data = json.load(json_file)
            finish_args = data["finish-args"]
            for arg in finish_args:
                if arg == "--filesystem=host" or arg == "--filesystem=home":
                    break

            else:
                finish_args.append("--filesystem={}".format(self.source_dir))
                finish_args.append("--filesystem={}".format(flatpak_dev_dir))

                if os.path.exists(os.path.expanduser("~/.bash_history")):
                    finish_args.append("--filesystem={}".format(os.path.expanduser("~/.bash_history")))

                if os.path.exists(os.path.expanduser("~/.bashrc")):
                    finish_args.append("--filesystem={}".format(os.path.expanduser("~/.bashrc")))

                finish_args.append("--nofilesystem=host")
                finish_args.append("--nofilesystem=home")
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()

            self.finish_args = finish_args

    def build_flatpak_module(self):
        if not os.path.exists(self.flatpak_build_dir):
            os.mkdir(self.flatpak_build_dir)
        command = ["flatpak-builder", "--force-clean","--stop-at={}".format(self.module_name),
                   self.flatpak_build_dir, self.modified_manifest]

        subprocess.run(command, cwd=self.cwd, check=True)

    def run_configure(self):
        command = ["flatpak-builder", "--run"] + self.finish_args + \
                  [self.flatpak_build_dir, self.modified_manifest] + \
                  self.configure_command

        subprocess.run(command, cwd=self.cwd, check=True)

    def run_make(self):
        command = ["flatpak-builder", "--run"] + self.finish_args + \
                  [self.flatpak_build_dir, self.modified_manifest] + \
                  self.make_command

        subprocess.run(command, cwd=self.cwd, check=True)

    def run_make_install(self):
        command = ["flatpak-builder", "--run"] + self.finish_args + \
                  [self.flatpak_build_dir, self.modified_manifest] + \
                  self.make_install_command

        subprocess.run(command, cwd=self.cwd, check=True)


class FlatpakModule:

    def __init__(self, module):
        self.name = module["name"]
        self.config_opts = module.get("config-opts", [])
        self.make_args = module.get("module-args", [])
        self.make_install_args = module.get("make-install-args", [])
        self.buildsystem = module.get("buildsystem", "autotools")
        self.build_options = module.get("build-options", {})

    def get_configure_command(self, source_dir, build_dir):
        if self.buildsystem == "autotools":
            if not os.path.exists(build_dir):
                os.mkdir(build_dir)

            # TODO: Check if autogen.sh calls configure
            files = os.listdir(source_dir)
            if "autogen.sh" in files:
                print("Autogen currently not supported")
            elif "configure" in files:
                opts = list(set(["--prefix=/app", "--libdir=/app/lib"] +
                            self.config_opts))
                configure = " ".join([os.path.join(source_dir, "configure")] + opts)
                commands = "cd {};{}".format(build_dir, configure)
                bash_script = "bash -c '{}'".format(commands)
                configure_command = shlex.split(bash_script)

        elif self.buildsystem == "meson":
            opts = list(set(["--prefix=/app", "--libdir=/app/lib"] +
                            self.config_opts))
            configure_command = ["meson", source_dir, build_dir] + opts

        return configure_command

    def get_make_command(self, build_dir):
        if self.buildsystem == "autotools":
            make = " ".join(["make"] + self.make_args)
            commands = "cd {};{}".format(build_dir, make)
            bash_script = "bash -c '{}'".format(commands)
            make_command = shlex.split(bash_script)
        elif self.buildsystem == "meson":
            make_command = ["ninja", "-C", build_dir] + \
                            self.make_args

        return make_command

    def get_make_install_command(self, build_dir):
        if self.buildsystem == "autotools":
            make_install = " ".join(["make", "install"] + self.make_install_args)
            commands = "cd {};{}".format(build_dir, make_install)
            bash_script = "bash -c '{}'".format(commands)
            make_install_command = shlex.split(bash_script)
        elif self.buildsystem == "meson":
            make_install_command = ["ninja", "-C",
                                    build_dir, "install"] + \
                                    self.make_install_args

        return make_install_command


class ProxyCommand:

    def __init__(self, argv):
        self.flatpak_dev = FlatpakDev()
        self.args = argv
        self.subparser = argv.subparser_name

    def install(self):
        self.flatpak_dev.install(args.sourceDir, self.args.json, self.args.name)

    def list(self):
        self.flatpak_dev.list_apps()

    def enter(self):
        self.flatpak_dev.enter_sandbox(self.args.name)

    def make(self):
        self.flatpak_dev.make_and_install(self.args.name)

    def run(self):
        if self.subparser == "install":
            self.install()
        elif self.subparser == "list":
            self.list()
        elif self.subparser == "enter":
            self.enter()
        elif self.subparser == "make":
            self.make()


def main():
    parser = argparse.ArgumentParser(
            description="Simple python wrapper of Flatpak-Builder")

    factory_parser = parser.add_subparsers(dest="subparser_name",
            description="Valid subcommands")
    factory_parser.required = True

    install_parser = factory_parser.add_parser("install")
    install_parser.add_argument("sourceDir", action="store")
    install_parser.add_argument("json", action="store")
    install_parser.add_argument("name", action="store", nargs="?")

    list_parser = factory_parser.add_parser("list")

    enter_parser = factory_parser.add_parser("enter")
    enter_parser.add_argument("name", action="store")

    make_parser = factory_parser.add_parser("make")
    make_parser.add_argument("name", action="store")

    args = parser.parse_args()

    proxy_command = ProxyCommand(args)
    proxy_command.run()
