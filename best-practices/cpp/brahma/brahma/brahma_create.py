#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import os

from git import Repo

import brahma.git_helpers as git_helpers
import brahma.log as log
import brahma.utils as utils
import brahma.brahma_init as brahma_init


def run(paths, settings, args):
    """
    Execute create step.

    :param paths: Relevant workspace paths
    :type paths: BrahmaWorkspacePaths
    :param settings: Workspace settings
    :type settings: BrahmaWorkspaceSettings
    :param args: Additonal Arguments parsed by argparse
    """
    settings.loadConfiguration(args.config)

    # Create folders
    log.title('Creating folder structure')
    log.prefixStatus('Creating source directory', '{}'.format(paths.source))
    utils.createDirectory(paths.source, args.force)
    log.prefixStatus('Creating catkin workspace directory', '{}'.format(paths.catkinSource()))
    utils.createDirectory(paths.catkinSource(), args.force)

    # Init repositories (abuse default settings repository for cloning)
    for repo in args.repository:
        settings.addRepository(repo[0], repo[1], repo[2])

    if settings.git_repositories:
        log.title('Creating repositories')
        git_helpers.cloneOrLinkRepositories(settings.git_repositories, paths.source)

    # Initialize the workspace
    brahma_init.init_workspace(paths, settings)

    # Save configuration
    log.title("Save workspace configuration")
    log.prefixStatus("Save to", "{}".format(paths.configurationDirectory()))
    settings.save(paths.workspace)


def setup_parser():
    """
    Parse create options.

    :returns: Parser with added arguments for the create step.
    """
    parser = argparse.ArgumentParser(prog='brahma create', description='\033[1mbrahma create [args]\033[0m\n Create a new workspace.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--force', help='Force folder generation.', action='store_true')
    parser.add_argument('-r', '--repository', help='Git repositories to clone.', metavar=("REPO_NAME", "REPO_URL", "REPO_BASE_BRANCH"),
                        nargs=3, action='append', default=[])
    parser.add_argument('--config', help='Configuration to load.', default="default")

    return parser
