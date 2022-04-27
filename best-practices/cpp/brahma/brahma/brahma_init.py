#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import os

from brahma.BrahmaWorkspacePaths import BrahmaWorkspacePaths
from brahma.BrahmaWorkspaceSettings import BrahmaWorkspaceSettings
from brahma.CatkinToolsOptions import CatkinToolsOptions
from brahma.CatkinWorkspace import CatkinWorkspace

import brahma.git_helpers as git_helpers
import brahma.log as log
import brahma.utils as utils


def run(paths, settings, args):
    """
    Execute init step.

    :param paths: Relevant workspace paths
    :type paths: BrahmaWorkspacePaths
    :param settings: Workspace settings
    :type settings: BrahmaWorkspaceSettings
    :param args: Additonal Arguments parsed by argparse
    """
    # Load settings
    settings.loadConfiguration(args.config)

    # Check settings
    if not os.path.isdir(os.path.join("/opt/ros/",settings.ros_distro)):
        log.error("ROS version '{}' is not installed. Update the configuration '{}' with an installed ROS version.".format(settings.ros_distro, args.config))

    if not os.path.isdir(paths.catkin):
        log.error("Catkin workspace '{}' does not exist. Can not initialize brahma workspace.".format(paths.catkin))

    if not os.path.isdir(paths.source):
        log.error("Source directory '{}' does not exist. Can not initialize brahma workspace.".format(paths.source))

    # Init workspace with settings
    init_workspace(paths, settings)

    log.title("Save workspace configuration")
    log.prefixStatus("Save to", "{}".format(paths.configurationDirectory()))
    settings.save(paths.workspace)


def init_workspace(paths, settings):

    # Init catkin workspace
    log.title('Initializing catkin workspace')
    catkin_options = CatkinToolsOptions(paths.catkin, settings.ros_distro)
    catkin_ws = CatkinWorkspace()
    catkin_ws.init(catkin_options)

    # Save workspace configuration
    log.title("Configuring brahma workspace")

    # Create configuration directory
    if not os.path.isdir(paths.configurationDirectory()):
        os.makedirs(paths.configurationDirectory())

    settings.summary()


def setup_parser():
    """
    Parse init options.

    :returns: Parser with added arguments for the init step.
    """
    parser = argparse.ArgumentParser(prog='brahma init', description='\033[1mbrahma init [args]\033[0m\n Initialize the workspace.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--config', help='Configuration to load.', default="default")

    return parser
