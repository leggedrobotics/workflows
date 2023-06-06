#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import fnmatch
import os
import shutil

from catkin_tools.context import Context
from catkin_tools.verbs.catkin_clean.clean import clean_packages
from catkin_tools.metadata import init_metadata_root
import catkin_tools.execution.job_server as job_server
from catkin_pkg.packages import find_packages

import brahma.log as log


class CatkinWorkspace:
    """
    The CatkinTools object handles the configuration of the catkin workspace.
    See catkin-tools python package for more information.
    """

    def __init__(self):
        self.context = None

    def load(self, catkin_options):
        """
        Load current catkin context.

        :param catkin_options: Options with which the catkin workspace should be initialized
        :type catkin_options: CatkinToolsOptions
        """
        job_server.initialize(
            max_jobs=1,
            max_load=None,
            gnu_make_enabled=False)
        self.context = Context.load(catkin_options.workspace, strict=True)

    def init(self, catkin_options):
        """
        Run 'catkin init' with the given options.

        :param catkin_options: Options with which the catkin workspace should be initialized
        :type catkin_options: CatkinToolsOptions
        """
        # Init catkin workspace
        self.context = Context.load(catkin_options.workspace, strict=True)
        if not self.context:
            init_metadata_root(catkin_options.workspace, catkin_options.reset)

        # Configure catkin workspace
        self.context = Context.load(catkin_options.workspace, catkin_options.profile, catkin_options)

        if self.context.initialized():
            Context.save(self.context)
            log.info(Context.summary(self.context))

    def cleanPackages(self, package_names):
        """
        Run 'catkin clean' for the given packages.

        :param package_names: List of package names to clean.
        :type package_names: list(str)
        """
        if self.usingInstallSpace():
            # Use the install manifest to clean the package.
            for package in package_names:
                install_manifest = os.path.join(self.buildSpace(), package, "install_manifest.txt")
                if not os.path.isfile(install_manifest):
                    log.warn("No install manifest found for package {}. Install space may be inconsistent.".format(package))
                else:
                    with open(install_manifest) as manifest:
                        pattern = self.installSpace() + "/**/**"
                        for file in manifest.readlines():
                            real_file = os.path.realpath(file.rstrip())
                            if fnmatch.fnmatch(real_file, pattern):
                                if os.path.isfile(real_file):
                                    os.remove(real_file)
                                else:
                                    log.warn("Can not remove file {}. Install space may be inconsistent.".format(real_file))

        # Use catkin tools clean function. If not yet possible force-clean the build space.
        clean_packages(self.context, package_names, False, True, False)

        # Force clean the build space.
        for package in package_names:
            package_build_path = os.path.join(self.context.build_space_abs, package)
            if os.path.isdir(package_build_path):
                log.info("Force cleaning package {}".format(package))
                shutil.rmtree(package_build_path)

    def getBuiltPackages(self):
        return find_packages(self.context.package_metadata_path(), exclude_subspaces=True, warnings=[])

    def workspace(self):
        return self.context.workspace

    def sourceSpace(self):
        return self.context.source_space_abs

    def buildSpace(self):
        return self.context.build_space_abs

    def develSpace(self):
        return self.context.devel_space_abs

    def installSpace(self):
        return self.context.install_space_abs

    def develOrInstallSpace(self):
        if self.usingInstallSpace():
            return self.installSpace()
        else:
            return self.develSpace()

    def usingInstallSpace(self):
        return self.context.install

    def extendPath(self):
        return self.context.extend_path

    def sourceFile(self, is_zsh):
        """
        Get the source file, depending on the shell type.

        :param is_zsh: Flag to determine file extension (true: zsh, false: sh)
        :type is_zsh: Bool
        """
        source_file = self.develOrInstallSpace()

        if is_zsh:
            source_file = os.path.join(source_file, 'setup.zsh')
        else:
            source_file = os.path.join(source_file, 'setup.bash')

        return source_file
