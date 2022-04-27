#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import os
import yaml

import brahma.git_helpers as git_helpers
import brahma.log as log
import brahma.summary as summary

WORKSPACE_CONFIGURATION_DIR = os.path.expanduser("~/.config/brahma")
WORKSPACE_CONFIGURATION_DEFAULTS = WORKSPACE_CONFIGURATION_DIR + "/default.yaml"
WORKSPACE_SETTINGS_FILE = "settings.yaml"


class BrahmaWorkspaceSettings:
    """
    The BrahmaWorkspaceSettings object contains all settings for the workspace

    :ivar include_upstream_dependencies: Flag to include upstream dependencies
    :type include_upstream_dependencies: bool
    :ivar include_downstream_dependencies: Flag to include downstream dependencies
    :type include_downstream_dependencies: bool
    :ivar include_missing_dependencies: Flag to include missing dependencies
    :type include_missing_dependencies: bool
    :ivar filter_packages: Add only packages in the package tree that are part of branches that end up in on of these packages.
    :vartype filter_packages: list(str)
    :ivar only_filter_downstream_packages: Only apply the filter packages to downstream packages.
    :vartype only_filter_downstream_packages: bool
    :ivar explicit_packages: Packages that are added to every workspace
    :vartype explicit_packages: list(str)
    :ivar git_repositories: Git repositories to clone and maintain (name, url)
    :vartype git_repositories: dict(str, str)
    :ivar ide: IDE for which to generate configuration files ("none" to skip)
    :vartype ide: str
    :ivar complete_overlay: Flag to create a complete catkin overlay with all packages found in the repositories
    :vartype complete_overlay: bool
    :ivar ros_distro: Deduced ROS distribution
    :vartype ros_distro: str
    """

    def __init__(self):

        self.filter_packages = []
        self.only_filter_downstream_packages = False
        self.explicit_packages = []

        self.include_upstream_dependencies = False
        self.include_downstream_dependencies = True
        self.include_missing_dependencies = False
        self.complete_overlay = False

        self.git_repositories = {}

        self.ide = "clion"
        self.ros_distro = ""

        # Load ros version
        ros_env = os.environ.get('ROS_DISTRO')

        if ros_env:
            # Use sourced ROS version
            self.ros_distro = ros_env
        else:
            ros_installation_dir = "/opt/ros"
            ros_versions = []
            if os.path.isdir(ros_installation_dir):
                ros_versions = os.listdir(ros_installation_dir)

            if len(ros_versions) == 0:
                log.error("No ROS version installed.")
            elif len(ros_versions) > 1:
                log.error("Multiple ROS versions installed. Source one of the versions and repeat the command.")
            else:
                # Use installed ROS version
                self.ros_distro = ros_versions[0]

        # Create default configuration if not existing
        self.createDefaultConfiguration(False)

    def addRepository(self, rel_path, url, base_branch):
        """
        Add the repository at 'rel_path'

        :param rel_path: Relative path of the repository in the git directory
        :type rel_path: str
        :param url: URL of the repository
        :type url: str
        :param base_branch: Base branch of the repository
        :type base_branch: str
        """
        self.git_repositories[rel_path] = [url, base_branch]

    def removeRepository(self, rel_path):
        """
        Remove the repository at 'rel_path'

        :param rel_path: Relative path of the repository in the git directory
        :type rel_path: str
        """
        self.git_repositories.pop(rel_path, None)

    def clearRepositories(self):
        """
        Remove all repositories
        """
        self.git_repositories.clear()

    def createDefaultConfiguration(self, force):
        """
        Create default workspace configuration file.

        :param force: Force if existing.
        :type force: str
        """
        existing = os.path.exists(WORKSPACE_CONFIGURATION_DEFAULTS)
        if not existing:
            if not os.path.exists(WORKSPACE_CONFIGURATION_DIR):
                os.makedirs(WORKSPACE_CONFIGURATION_DIR)
        if not existing or force:
            with open(WORKSPACE_CONFIGURATION_DEFAULTS, 'w') as f:
                yaml.dump(self.__dict__, f)

    def loadConfiguration(self, configuration="default"):
        """
        Load a specific workspace configuration from a yaml file.

        :param configuration: Name of the configuration (has to be placed in WORKSPACE_CONFIGURATION_DIR)
        :type configuration: str
        """
        configurationFile = WORKSPACE_CONFIGURATION_DIR + "/" + configuration + ".yaml"
        with open(configurationFile, 'r') as f:
            self.__dict__.update(yaml.full_load(f))

    def settingsFile(self, workspace_dir):
        """
        :param workspace_dir: Workspace directory.
        :type workspace_dir: str
        :returns: Path of the settings file
        :rtype: str
        """
        return workspace_dir + '/.brahma/' + WORKSPACE_SETTINGS_FILE

    def load(self, workpace_dir):
        """
        Load the workspace settings from a yaml file
        """
        with open(self.settingsFile(workpace_dir), 'r') as f:
            self.__dict__.update(yaml.full_load(f))

    def save(self, workpace_dir):
        """
        Save the workspace paths to a yaml file.
        :param workpace_dir: Workspace directory.
        :type workpace_dir: str
        """
        # Make sure lists are alphabetical
        if self.filter_packages:
            self.filter_packages.sort(key=str.lower)
        if self.explicit_packages:
            self.explicit_packages.sort(key=str.lower)
        with open(self.settingsFile(workpace_dir), 'w') as f:
            yaml.dump(self.__dict__, f)

    def summary(self):
        """
        Print a summary of the current settings
        """
        log.info("-" * 50)
        for key, value in sorted(self.__dict__.items()):
            if isinstance(value, list) or isinstance(value, set):
                summary.entry(key, "")
                for v in sorted(value):
                    summary.entry("", "- " + v)
            elif isinstance(value, dict):
                summary.entry(key, "")
                for k, v in sorted(value.items()):
                    if isinstance(v, list) or isinstance(v, set):
                        summary.entry("", "- " + k + " :")
                        for i in v:
                            summary.entry("", '    ' + i)
                    else:
                        summary.entry("", "- " + k + " : " + v)
            else:
                summary.entry(key, value)
        log.info("-" * 50)
        return
