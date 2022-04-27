#!/usr/bin/python3

# Data:         06.05.2019
# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import sys
import os

import brahma.log as log
import brahma.utils as utils

from brahma.BrahmaWorkspacePaths import BrahmaWorkspacePaths as BrahmaWorkspacePaths
from brahma.BrahmaWorkspaceSettings import BrahmaWorkspaceSettings as BrahmaWorkspaceSettings

import brahma.brahma_config as brahma_config
import brahma.brahma_create as brahma_create
import brahma.brahma_init as brahma_init
import brahma.brahma_update as brahma_update
import brahma.brahma_info as brahma_info
import brahma.brahma_clean as brahma_clean

# Setup verbs
verbs = ['create', 'init', 'config', 'update', 'setup', 'info', 'clean']


def brahma_main():
    """
    Main function of the brahma script.
    Calls fucntions depending on the selected verb.
    """
    # Use main parser to determine verb
    main_parser = argparse.ArgumentParser(
        description='brahma is a managing tool for catkin workspaces that are version controlled with git.\n',
        formatter_class=argparse.RawTextHelpFormatter)
    main_parser.add_argument("verb", help=', '.join(verbs))
    main_args = main_parser.parse_args(sys.argv[1:2])
    verb = main_args.verb

    # Error on no verb provided
    if verb is None:
        log.error("No verb provided.")
        main_parser.print_help()

    # Error on unknown verb provided
    if verb not in verbs:
        log.error("Unknown verb '{0}' provided.".format(main_args.verb))
        main_parser.print_help()

    # Create default config
    if verb == verbs[4]:
        BrahmaWorkspaceSettings().createDefaultConfiguration(True)
        return

    # Parse verb arguments
    if verb == verbs[0]:  # Create
        parser = brahma_create.setup_parser()
    elif verb == verbs[1]:  # Init
        parser = brahma_init.setup_parser()
    elif verb == verbs[2]:  # Config
        parser = brahma_config.setup_parser()
    elif verb == verbs[3]:  # Update
        parser = brahma_update.setup_parser()
    elif verb == verbs[5]:  # Source
        parser = brahma_info.setup_parser()
    elif verb == verbs[6]:  # Clean
        parser = brahma_clean.setup_parser()

    # Common arguments
    parser.add_argument("workspace", help='Full path of the workspace.', nargs='?', default=None)
    parser.add_argument('--quiet', '-q', help='Disable verbose output.', action='store_true')
    args = parser.parse_args(sys.argv[2:])

    # Get workspace path
    if verb == verbs[0]:
        # Create has no settings file yet -> use provided path
        if args.workspace:
            workspace_path = args.workspace
        else:
            log.error("No workspace path provided to create.")
    else:
        if not args.workspace:
            args.workspace = os.getcwd()

        workspace_path = utils.getWorkspacePath(args.workspace)
        # Init does not necessarily have a config file yet use provided folder
        if not workspace_path and verb == verbs[1]:
            workspace_path = args.workspace

        # Check if workspace exists
        if not workspace_path or not os.path.isdir(workspace_path):
            log.error("Could not find workspace.")

    # Get settings from default configuration
    settings = BrahmaWorkspaceSettings()
    settings.loadConfiguration()

    # Set default workspace
    paths = BrahmaWorkspacePaths(workspace_path)

    # IMPORTANT: No info output before this point, otherwise brahma info breaks.
    utils.createDirectory(paths.log(), True)
    log.setupLogger(args.quiet, paths.log(), "brahma")

    # Execute action
    if verb == verbs[0]:  # Create
        brahma_create.run(paths, settings, args)
    elif verb == verbs[1]:  # Init
        brahma_init.run(paths, settings, args)
    elif verb == verbs[2]:  # Config
        brahma_config.run(paths, settings, args)
    elif verb == verbs[3]:  # Update
        brahma_update.run(paths, settings, args)
    elif verb == verbs[5]:  # Info
        brahma_info.run(paths, settings, args)
    elif verb == verbs[6]:  # Clean
        brahma_clean.run(paths, settings, args)
    log.title('Done')


if __name__ == '__main__':
    try:
        brahma_main()
    except KeyboardInterrupt:
        log.warn('Interrupted by user!')
