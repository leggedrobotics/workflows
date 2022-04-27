#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import os


class CatkinToolsOptions:
    """
    The CatkinToolsOptions object contains the configuration for the catkin workspace.
    Per default extend opt/ros and use release mode to build.
    See catkin-tools python package for more information.
    """

    def __init__(self, workspace, ros_distro):
        self.workspace = workspace
        self.reset = False
        self.profile = None
        self.extend_path = "/opt/ros/" + ros_distro
        self.source_space = None
        self.log_space = None
        self.build_space = None
        self.devel_space = None
        self.install_space = None
        self.devel_layout = None
        self.install = False
        self.isolate_install = False
        self.cmake_args = ["-DCMAKE_BUILD_TYPE=RelWithDebInfo"]
        self.make_args = None
        self.jobs_args = None
        self.use_internal_make_jobserver = True
        self.use_env_cache = False
        self.catkin_make_args = None
        self.space_suffix = None
        self.whitelist = None
        self.blacklist = None
