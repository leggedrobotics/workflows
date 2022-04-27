#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import os
import yaml

WORKSPACE_PATHS_FILE = "paths.yaml"


class BrahmaWorkspacePaths:
    """
    The BrahmaWorkspacePaths object contains all relevant paths of the workspace

    :param workspace_path: Root path of the workspace
    :type workspace_path: str
    :ivar workspace: Root path of the workspace
    :vartype arg: str
    :ivar catkin: Catkin workspace directory
    :vartype catkin: str
    :ivar source: Source code directory with IDE configurations
    :vartype source: str
    """

    def __init__(self, workspace_path):
        self.workspace = os.path.abspath(os.path.realpath(workspace_path))
        self.catkin = self.workspace + "/catkin_ws"
        self.source = self.workspace + "/source"

    def catkinSource(self):
        '''
        :returns: Catkin source directory
        :rtype: str
        '''
        return self.catkin + "/src"

    def configurationDirectory(self):
        '''
        :returns: Directory of the configuration files
        :rtype: str
        '''
        return self.workspace + '/.brahma/'

    def configurationFile(self):
        '''
        :returns: Path of the configuration file
        :rtype: str
        '''
        return self.configurationDirectory() + WORKSPACE_PATHS_FILE

    def log(self):
        '''
        :returns: Log file directory
        :rtype: str
        '''
        return self.configurationDirectory()

    def save(self):
        '''
        Save the workspace paths to a yaml file.
        '''
        self.catkin = os.path.relpath(self.catkin, self.workspace)
        self.source = os.path.relpath(self.source, self.workspace)
        with open(self.configurationFile(), 'w') as f:
            yaml.dump(self.__dict__, f)

    def load(self):
        '''
        Load the workspace paths from a yaml file.
        '''
        self.catkin = os.path.abspath(os.path.realpath(os.path.join(self.workspace, self.catkin)))
        self.source = os.path.abspath(os.path.realpath(os.path.join(self.workspace, self.source)))
        with open(self.configurationFile(), 'r') as f:
            self.__dict__.update(yaml.full_load(f))
