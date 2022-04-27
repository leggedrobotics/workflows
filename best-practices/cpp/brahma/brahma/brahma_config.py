#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import os
import sys

from brahma.BrahmaWorkspacePaths import BrahmaWorkspacePaths
from brahma.BrahmaWorkspaceSettings import BrahmaWorkspaceSettings

import brahma.log as log


def run(paths, settings, args):
    """
    Execute config step.

    :param paths: Relevant workspace paths
    :type paths: BrahmaWorkspacePaths
    :param settings: Workspace settings
    :type settings: BrahmaWorkspaceSettings
    :param args: Additonal Arguments parsed by argparse
    """
    # Load configuration from file
    settings.load(paths.workspace)

    # Set configuration
    if args.upstream_deps:
        settings.include_upstream_dependencies = True
    if args.no_upstream_deps:
        settings.include_upstream_dependencies = False

    if args.downstream_deps:
        settings.include_downstream_dependencies = True
    if args.no_downstream_deps:
        settings.include_downstream_dependencies = False

    if args.missing_deps:
        settings.include_missing_dependencies = True
    if args.no_missing_deps:
        settings.include_missing_dependencies = False

    if args.no_filter_packages:
        settings.filter_packages = []
    else:
        package_set = set(settings.filter_packages)
        package_set.update(args.add_filter_packages)
        package_set.difference_update(args.remove_filter_packages)
        settings.filter_packages = list(package_set)

    if args.filter_only_downstream_packages:
        settings.only_filter_downstream_packages = True
    if args.filter_all_packages:
        settings.only_filter_downstream_packages = False

    if args.no_explicit_packages:
        settings.explicit_packages = []
    else:
        package_set = set(settings.explicit_packages)
        package_set.update(args.add_explicit_packages)
        package_set.difference_update(args.remove_explicit_packages)
        settings.explicit_packages = list(package_set)

    if args.ide is not None:
        settings.ide = args.ide
    if args.ros_distro is not None:
        settings.ros_distro = args.ros_distro

    # Save workspace configuration
    log.title("Brahma workspace configuration")
    settings.summary()
    settings.save(paths.workspace)


def setup_parser():
    """
    Parse config options.

    :returns: Parser with added arguments for the config step.
    """
    parser = argparse.ArgumentParser(prog='brahma config',
                                     description='\033[1mbrahma configure [args]\033[0m\n Configure the workspace.',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '--upstream-deps', help='Adds all upstream dependencies of the packages to the workspace.', action='store_true')
    parser.add_argument(
        '--no-upstream-deps', help='Do not add upstream dependencies of the packages to the workspace.',
        action='store_true')
    parser.add_argument(
        '--downstream-deps', help='Adds all downstream dependencies of the packages to the workspace.',
        action='store_true')
    parser.add_argument('--no-downstream-deps',
                        help='Do not add downstream dependencies of the packages to the workspace.',
                        action='store_true')
    parser.add_argument(
        '--missing-deps', help='Adds all dependencies that are not installed to the workspace.', action='store_true')
    parser.add_argument('--no-missing-deps',
                        help='Do not add all dependencies that are not installed to the workspace.',
                        action='store_true')

    parser.add_argument("--add-filter-packages", nargs="+",
                        help='Add package to the list of packages that are used to filter the package tree.', type=str,
                        default=list())
    parser.add_argument("--remove-filter-packages", nargs="+",
                        help='Remove package from the list of packages that are used to filter the package tree.',
                        type=str, default=list())
    parser.add_argument("--no-filter-packages",
                        help='Clear list of packages that are used to filter the package tree.', action='store_true')

    parser.add_argument("--filter-only-downstream-packages",
                        help='Limit the filtering of packages to downstream packages.', action='store_true')
    parser.add_argument("--filter-all-packages",
                        help='Apply the filtering of packages to all packages.', action='store_true')

    parser.add_argument("--add-explicit-packages", nargs="+",
                        help='Add packages to the list of packages explicitly added to the workspace.', type=str,
                        default=list())
    parser.add_argument("--remove-explicit-packages", nargs="+",
                        help='Remove packages from the list of packages explicitly added to the workspace.', type=str,
                        default=list())
    parser.add_argument("--no-explicit-packages",
                        help='Clear list of packages explicitly added to the workspace.', action='store_true')

    parser.add_argument("--ide", help='Generate project files for this IDE. Choose "none" to skip.',
                        default=None, choices=["none", "clion"])
    parser.add_argument(
        "--ros-distro", help='ROS distribution.', default=None)
    return parser
