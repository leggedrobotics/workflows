#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import os
import sys

from brahma.BrahmaWorkspacePaths import BrahmaWorkspacePaths
from brahma.BrahmaWorkspaceSettings import BrahmaWorkspaceSettings
from brahma.CatkinToolsOptions import CatkinToolsOptions
from brahma.CatkinWorkspace import CatkinWorkspace

import brahma.log as log


def run(paths, settings, args):
    """
    Execute clean step.

    :param paths: Relevant workspace paths
    :type paths: BrahmaWorkspacePaths
    :param settings: Workspace settings
    :type settings: BrahmaWorkspaceSettings
    :param args: Additional arguments parsed by argparse
    """

    # Load configuration from file
    settings.load(paths.workspace)

    # Clean packages
    if args.packages:
        catkin_options = CatkinToolsOptions(paths.catkin, settings.ros_distro)
        catkin_ws = CatkinWorkspace()
        catkin_ws.load(catkin_options)
        catkin_ws.cleanPackages(args.packages)
        settings.include_upstream_dependencies = True


def setup_parser():
    """
    Parse clean options.

    :returns: Parser with added arguments for the clean step.
    """
    parser = argparse.ArgumentParser(prog='brahma clean',
                                     description='\033[1mbrahma clean --packages [packages]\033[0m\n Clean packages. Also works for install spaces. ',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--packages', nargs="+", metavar='PACKAGE',
                        help='List of packages to be cleaned.', type=str, default=list())

    return parser
