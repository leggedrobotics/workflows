#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import argparse
import os

from brahma.BrahmaWorkspacePaths import BrahmaWorkspacePaths
from brahma.BrahmaWorkspaceSettings import BrahmaWorkspaceSettings
from brahma.CatkinToolsOptions import CatkinToolsOptions
from brahma.CatkinWorkspace import CatkinWorkspace

import brahma.ide.clion as clion
import brahma.git_helpers as git_helpers
import brahma.log as log
import brahma.utils as utils


def run(paths, settings, args):
    """
    Execute update step.

    :param paths: Relevant workspace paths
    :type paths: BrahmaWorkspacePaths
    :param settings: Workspace settings
    :type settings: BrahmaWorkspaceSettings
    :param args: Additonal Arguments parsed by argparse
    """
    if args.pull_and_merge:
        args.pull = True

    # Load configuration from file
    settings.load(paths.workspace)

    log.title('Initializing git repositories')

    # Clone missing repositories
    git_helpers.cloneOrLinkRepositories(settings.git_repositories, paths.source)

    # Setup git repos from folder
    repos = git_helpers.getRepositories(paths.source)
    for repo in repos:
        repo_rel_path = os.path.relpath(repo, paths.source)
        if not repo_rel_path in settings.git_repositories.keys():
            log.warn("Untracked repository '{}' found. Not resolving diff.".format(os.path.basename(repo)))

    # Package collections needed for catkin and ide folder update
    catkin_packages = dict()

    # Gather filter packages information
    if settings.filter_packages:
        log.title('Initialize filter packages')
        log.info('Resolve dependencies of the filter packages ...')
        filter_packages = utils.getPackagesFromPackageNames(settings.filter_packages, paths.source)
        filter_packages_tree = utils.getRecursiveUpstreamDependencies(filter_packages, paths.source)

    # Handle complete overlay
    if settings.complete_overlay:
        # Complete overlay - Add all packages to the catkin workspace.
        log.title('Resolve complete overlay')
        all_packages = utils.getAllPackagesFromDirectory(paths.source)
        catkin_packages = all_packages

    else:
        # Resolve packages from diff (only if there is a base_branch)
        diff_packages = dict()
        for repo, repo_info in settings.git_repositories.items():
            log.title("Process repository '{}'".format(repo))

            repo_url = repo_info[0]
            repo_base_branch = repo_info[1]
            if repo_base_branch:
                repo_path = os.path.join(paths.source, repo)
                git_repo = git_helpers.getRepository(repo_path)
                os.chdir(repo_path)

                # Pull branches
                if args.pull:
                    # Fetch remotes
                    for remote in git_repo.remotes:
                        remote.fetch()

                    if git_repo.head.is_detached:
                        log.warn("HEAD is detached for repository '{}'. Not pulling latest changes.".format(repo))
                    else:
                        current_branch = git_repo.active_branch.name

                        stash_name = "brahma_update"
                        log.status("Stash")
                        log.info("Stash changes of branch '{}'.".format(current_branch))
                        stash_return = git_helpers.stashChanges(git_repo, stash_name)
                        log.info(stash_return)
                        log.status("Pull")
                        if current_branch != repo_base_branch:
                            log.info("Update base branch '{}'.".format(repo_base_branch))
                            git_helpers.pullBranch(git_repo, repo_base_branch)
                        log.info("Update current branch '{}'.".format(current_branch))
                        log.info(git_helpers.checkoutBranch(git_repo, current_branch, True))
                        if current_branch != repo_base_branch and args.pull_and_merge:
                            log.status("Merge")
                            log.info("Merge base branch '{}' into current branch '{}'.".format(repo_base_branch,
                                                                                               current_branch))
                            log.info(git_helpers.mergeBranch(git_repo, repo_base_branch))
                        if git_helpers.hasStash(stash_return, stash_name):
                            log.status("Re-apply stash")
                            log.info("Re-apply stashed changes of branch '{}'.".format(current_branch))
                            log.info(git_helpers.popStash(git_repo))
                else:
                    # Check if base branch exists
                    if repo_base_branch not in git_repo.refs:
                        log.status("Checkout")
                        log.info('Initial checkout of base branch {}.'.format(repo_base_branch))
                        current_branch = git_repo.active_branch.name
                        git_helpers.checkoutBranch(git_repo, repo_base_branch, False)
                        git_helpers.checkoutBranch(git_repo, current_branch, False)

                log.status("Check for deleted headers")
                utils.warnIfDeletedHeaders(git_repo, repo_base_branch)

                log.status("Resolve 'git diff'")
                diff = utils.getDiffToBaseBranch(git_repo, repo_base_branch)
                packages = utils.getPackagesFromFileList(diff, paths.source)
                if packages:
                    log.info('Resolved {} packages from the diff'.format(len(packages)))
                    log.packages(packages)

                diff_keys = set(diff_packages.keys())
                keys = set(packages.keys())
                if diff_keys.intersection(keys):
                    log.error("Multiple git repositories contain the same packages [{}]" +
                              ', '.join(p.name for p in diff_keys.intersection(keys)))
                diff_packages.update(packages)

        # Resolve upstream packages
        upstream_packages = dict()
        if settings.include_upstream_dependencies and diff_packages:
            log.title('Resolve upstream dependencies')
            upstream_packages = utils.getRecursiveUpstreamDependencies(diff_packages, paths.source)
            log.info('Resolved {} recursive upstream packages'.format(len(upstream_packages)))
            log.packages(upstream_packages)

        # Resolve downstream packages
        downstream_packages = dict()
        if settings.include_downstream_dependencies and diff_packages:
            log.title('Resolve downstream dependencies')
            downstream_packages = utils.getRecursiveDownstreamDependencies(diff_packages, paths.source)

            # Filter downstream packages
            if settings.filter_packages and settings.only_filter_downstream_packages and downstream_packages:
                log.info('Filter downstream packages')
                downstream_packages = utils.getFilteredPackages(downstream_packages, filter_packages,
                                                                filter_packages_tree)

            log.info('Resolved {} recursive downstream packages'.format(len(downstream_packages)))
            log.packages(downstream_packages)

        # Get dictionary of all packages
        catkin_packages = {**diff_packages, **upstream_packages, **downstream_packages}

    # Filter all packages
    if settings.filter_packages and not settings.only_filter_downstream_packages and catkin_packages:
        log.title('Filter packages')
        catkin_packages = utils.getFilteredPackages(catkin_packages, filter_packages, filter_packages_tree)
        log.info('{} packages remaining after filtering'.format(len(catkin_packages)))
        log.packages(catkin_packages)

    # Add explicit packages
    explicit_packages = dict()
    if settings.explicit_packages:
        log.title('Resolve explicit packages')
        explicit_packages = utils.getPackagesFromPackageNames(settings.explicit_packages, paths.source)
        log.info('Resolved {} explicit packages'.format(len(explicit_packages)))
        log.packages(explicit_packages)
        catkin_packages.update(explicit_packages)

    # Identify missing upstream packages
    if catkin_packages:
        log.title('Resolve missing upstream dependencies')
        install_path = "/opt/ros/" + settings.ros_distro + "/share"
        missing_packages = utils.getNotInstalledUpstreamDependencies(catkin_packages, paths.source, install_path)
        if missing_packages:
            log.info('Resolved {} missing upstream packages'.format(len(missing_packages)))
            log.packages(missing_packages)
            if settings.include_missing_dependencies:
                catkin_packages.update(missing_packages)
            else:
                log.warn(
                    'Configuration for "include_missing_dependencies" is set to "false". Will not add missing dependencies.')

    # Load catkin workspace
    catkin_options = CatkinToolsOptions(paths.catkin, settings.ros_distro)
    catkin_ws = CatkinWorkspace()
    catkin_ws.load(catkin_options)

    if settings.ide == "clion":
        log.title('Update clion')
        log.info('Create project files.')
        clion.setupCLionProject(paths.source, paths.source, os.path.basename(paths.workspace),
                                catkin_packages, catkin_ws)
        log.info('Setup clang tooling.')
        clion.createClangToolsSymlinks(paths.source)

    # Complete overlay adds all packages to workspace
    if settings.complete_overlay:
        catkin_packages = all_packages

    # Update and clean packages
    log.title('Update catkin workspace')
    utils.updateAndCleanPackages(catkin_packages, catkin_ws, paths.source)
    log.info('Adding {} packages to the workspace'.format(len(catkin_packages)))
    log.packages(catkin_packages)

    # Save workspace configuration
    settings.save(paths.workspace)


def setup_parser():
    """
    Parse update options.

    :returns: Parser with added arguments for the update step.
    """
    parser = argparse.ArgumentParser(prog='brahma update', description='\033[1mbrahma update [args]\033[0m\n'
                                                                       'Update the workspace.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--pull", help='Pull changes from the remote for the current branch and the base branch.', action='store_true')
    parser.add_argument(
        "--pull-and-merge",
        help='Pull changes from the remote for the current branch and the base branch. Merge base branch into the current branch.',
        action='store_true')
    return parser
