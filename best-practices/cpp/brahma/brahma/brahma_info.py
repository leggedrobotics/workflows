#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import os

from brahma.CatkinToolsOptions import CatkinToolsOptions
from brahma.CatkinWorkspace import CatkinWorkspace

import brahma.log as log
import brahma.utils as utils

properties = ['source_dir', 'catkin_dir', 'source_file']


def run(paths, settings, args):
    """
    Execute info step.

    :param paths: Relevant workspace paths
    :type paths: BrahmaWorkspacePaths
    :param settings: Workspace settings
    :type settings: BrahmaWorkspaceSettings
    :param args: Additonal Arguments parsed by argparse
    """
    catkin_options = CatkinToolsOptions(paths.catkin, settings.ros_distro)
    catkin_ws = CatkinWorkspace()
    catkin_ws.load(catkin_options)

    if args.property == properties[0]:  # source dir
        print(paths.source)
    elif args.property == properties[1]:  # catkin dir
        print(paths.catkin)
    elif args.property == properties[2]:  # source file
        is_zsh = False
        shell = os.environ.get('SHELL')
        if shell:
            is_zsh = shell.endswith("zsh")
        print(catkin_ws.sourceFile(is_zsh))

    exit(0)


def setup_parser():
    """
    Parse info options.

    :returns: Parser with added arguments for the info step.
    """
    parser = argparse.ArgumentParser(prog='brahma info', description='\033[1mbrahma info [args]\033[0m\n Print infos about the workspace.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("property", help=', '.join(properties))

    return parser
