#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import em
import os
import re
import shutil
import sys

from catkin_pkg import packages as catkin_pkgs
from catkin_pkg.packages import find_packages
from catkin_pkg.topological_order import topological_order_packages
from catkin_pkg.topological_order import topological_order

from catkin_tools.common import get_recursive_build_depends_in_workspace
from catkin_tools.common import get_recursive_run_depends_in_workspace
from catkin_tools.common import get_recursive_build_dependents_in_workspace
from catkin_tools.common import get_recursive_run_dependents_in_workspace

import brahma.log as log
from brahma.CatkinToolsOptions import CatkinToolsOptions
from brahma.CatkinWorkspace import CatkinWorkspace

try:
    import git
    from git import Repo
except:
    log.error(
        "The current directory does not exist in the base branch. Try to run the command from the root of your brahma workspace.")


###########################
### Filesystem utils    ###
###########################


def getWorkspacePath(dir):
    """
    Searches parent directories for ".brahma" folder.

    :param dir: Directory for which to deduce the workspace.
    :type dir: str
    :returns: Root path of the workspace of which 'dir' is part of, 'None' if 'dir' is not part of a workspace
    :rtype: str
    """
    path = os.path.abspath(os.path.realpath(dir))
    while path != "/":
        if os.path.isdir(path + "/.brahma"):
            return path
        path = os.path.dirname(path)
    return None


def createDirectory(dir, force):
    """
    Creates a directory. Exits the process if folder already exists.

    :param dir: Path of the directory to create
    :type dir: str
    :param force: If 'true' no error is triggered if the folder already exists.
    :type force: bool
    """
    if os.path.exists(dir):
        if not force:
            log.error("Workspace folder {} exists.".format(dir))
    else:
        os.makedirs(dir)


def updateSymlink(path, destination_dir):
    """
    Update (delete and recreate) a symlink to 'path' in 'destination_dir'

    :param path: File or folder to link
    :type path: str
    :param destination_dir: Directory in which to create the symbolic link
    :type destination_dir: str
    """
    destination_folder = os.path.join(destination_dir, os.path.basename(path))
    if os.path.islink(destination_folder):
        os.unlink(destination_folder)
    os.symlink(os.path.relpath(path, destination_dir), destination_folder)


def updateAndCleanPackages(packages, catkin_ws, packages_dir):
    """
    Remove all symlinks in 'catkin_ws' and add new symlinks to all 'packages'

    :param packages: Packages to link
    :type packages: dict(str,catkin_pkg.Package)
    :param catkin_ws: Catkin workspace handle.
    :type catkin_ws: CatkinWorkspace
    """
    # Packages that are present in the current workspace
    existing_packages = set([file for file in os.listdir(catkin_ws.sourceSpace())
                             if os.path.islink(os.path.join(catkin_ws.sourceSpace(), file))])
    # Packages that are built in the current workspace (ignore catkin_tools_prebuild)
    built_packages = set(catkin_ws.getBuiltPackages().keys())
    if 'catkin_tools_prebuild' in built_packages:
        built_packages.remove("catkin_tools_prebuild")
    # Packages that are built but not present in the current workspace
    dangling_packages = set(built_packages - set(existing_packages))
    # Packages that were removed in the current update
    removed_packages = set(existing_packages - set(packages.keys()))
    # Packages that were added in the current update
    added_packages = set(packages.keys() - set(existing_packages))
    # Packages that are persisting since the last update
    kept_packages = set(existing_packages & set(packages.keys()))

    # Check for moved packages since the last update
    moved_packages = set()
    for pkg_name in kept_packages:
        pkg_relative_path = os.readlink(os.path.join(catkin_ws.sourceSpace(), pkg_name))  # Is a relative symlink
        pkg_path = os.path.abspath(os.path.realpath(os.path.join(catkin_ws.sourceSpace(), pkg_relative_path)))
        if pkg_path != os.path.dirname(packages[pkg_name].filename):
            moved_packages.add(pkg_name)

    log.status("Prepare cleaning of catkin workspace")

    # Clean packages that are no longer part of the catkin workspace
    packages_to_clean = set(removed_packages)

    # Clean packages that are dangling
    packages_to_clean = set(packages_to_clean | dangling_packages)

    # Clean downstream packages if upstream dependencies are added or built packages were removed
    changed_packages = set(added_packages)
    for removed_package in removed_packages:
        if removed_package in built_packages:
            changed_packages.add(removed_package)

    if changed_packages:
        log.info('Resolve downstream packages of newly added or removed packages.')
        changed_packages_downstream_deps = getRecursiveDownstreamDependenciesFromNames(changed_packages, packages_dir)
        existing_changed_packages_downstream_deps = (set(changed_packages_downstream_deps.keys()) & existing_packages)
        packages_to_clean = set(packages_to_clean | existing_changed_packages_downstream_deps)
        log.info('Resolved {} downstream packages of newly added or removed packages'.format(
            len(existing_changed_packages_downstream_deps)))
        log.packages(existing_changed_packages_downstream_deps)

    # Only clean existing packages
    packages_to_clean = set(packages_to_clean & built_packages)
    if packages_to_clean:
        log.status("Clean catkin workspace")
        log.info('Resolved {} packages to clean'.format(len(packages_to_clean)))
        log.packages(packages_to_clean)
        catkin_ws.cleanPackages(list(packages_to_clean))

    # Update symbolic links
    log.status('Update symbolic links')
    for package_name in (removed_packages | moved_packages):
        os.unlink(os.path.join(catkin_ws.sourceSpace(), package_name))

    for package_name in (added_packages | moved_packages):
        package = packages[package_name]
        os.symlink(os.path.relpath(os.path.dirname(package.filename), catkin_ws.sourceSpace()),
                   catkin_ws.sourceSpace() + "/" + package.name)


###########################
### File diff utils     ###
###########################

def getDiffToBaseBranch(repo, base_branch):
    """
    Returns a list of changed files by comparing the current repository state against a 'base_branch'.
    This includes untracked and unstaged changes.

    :param repo: Git repository
    :type repo: git.Repo
    :param base_branch: Branch against which the current state should be compared
    :type base_branch: str
    :returns: A list of edited files (all files in git diff)
    :rtype: list of str
    """
    log.info('Looking up diff to base branch {}.'.format(base_branch))
    base_branch_commit = repo.commit(base_branch)
    diffPaths = [item.a_path for item in repo.index.diff(base_branch_commit)] + \
                [item.a_path for item in repo.index.diff(None)] + repo.untracked_files
    git_root = repo.git.rev_parse("--show-toplevel")
    diffPaths = [git_root + "/" + s for s in diffPaths]
    return diffPaths


def warnIfDeletedHeaders(repo, base_branch):
    """
    Warn the user about changed headerfiles that were deleted in the current repo state but are present in the 'base_branch'.
    This also includes unstaged changes.

    :param repo: Git repository
    :type repo: git.Repo
    :param base_branch: Branch against which the current state should be compared
    :type base_branch: str
    """
    log.info(
        'Checking diff to base branch {} for deleted headers.'.format(base_branch))
    # Check uncommited files
    headers = listHeadersInDiff(repo.index.diff(None), 'D')
    # Check commited files (Check for added files -> direction of the diff is different)
    headers = headers + listHeadersInDiff(repo.index.diff(repo.commit(base_branch)), 'A')

    if headers:
        log.warn(
            'Found deleted header files. Overlaying could lead to unexpected behavior, the headers files are still present in debians.')
        log.info('{}'.format("\n".join(headers)))


def listHeadersInDiff(diff, change_type):
    """
    Returns a list of all header files in 'diff' that have the give 'change_type'
    :param diff: Git diff to analyze

    :type diff: git.diff.DiffIndex
    :param change_type: Change type see git.diff.DiffIndex.change_type for options
    :type change_type: str
    :returns: A list of header files
    :rtype: list(str)
    """
    headers = []
    header_file_regex = re.compile('^.*(\.tpp|\.h|\.hh|\.hpp)$')
    for item in diff.iter_change_type(change_type):
        if header_file_regex.match(item.a_path):
            headers.append(item.a_path)
    return headers


###########################
### Package utils       ###
###########################

def getPackages(dir):
    """
    Returns a dictionary of catkin packages in 'dir'

    :param dir: Directory for which to list catkin packages
    :type dir: str
    :returns: A dictiornary of catkin packages
    :rtype: dict(str,catkin_pkg.Package)
    """
    return find_packages(dir, exclude_subspaces=True, warnings=[])


def getPackagePath(dir, package_name):
    """
    Returns the path of the package with name 'package_name'

    :param dir: Directory in which catkin package is located
    :type dir: str
    :returns: Package path of package with name 'package_name'
    :rtype: catkin_pkg.Package
    """
    return [pkg_path for pkg_path, p in getPackages(dir).items() if p.name == package_name]


def getAllPackagesFromDirectory(package_dir):
    """
    Get dictionary of catkin packages from a directory.

    :param package_dir: Directory in which packages are searched.
    :type package_dir: str
    :return: dict(str,catkin_pkg.Package)
    """
    packages = dict()
    catkin_packages = getPackages(package_dir)
    for path, catkin_package in catkin_packages.items():
        packages[catkin_package.name] = catkin_package

    return packages


def getPackagesFromFileList(files, package_dir):
    """
    Get dictionary of catkin packages from a list of file names.

    :param files: List of files
    :type files: list(str)
    :param package_dir: Directory in which packages are searched.
    :type package_dir: str
    :returns: All catkin packages found in directory 'package_dir' for which a file is in 'files'
    :rtype: dict(str,catkin_pkg.Package)
    """
    log.info('Resolve packages from diff.')
    packages = dict()
    catkin_packages = getPackages(package_dir)
    for file in files:
        for path, catkin_package in catkin_packages.items():
            if file.startswith(os.path.dirname(os.path.abspath(os.path.realpath(catkin_package["filename"]))) + '/'):
                packages[catkin_package.name] = catkin_package

    return packages


def getPackagesFromPackageNames(package_names, package_dir):
    """
    Get set of catkin packages from a list of package names.

    :param package_names: List of package names.
    :type package_names: list(str)
    :param package_dir: Directory in which packages are searched.
    :type package_dir: str
    :returns: All catkin packages found in directory 'package_dir' contained in 'package_names'
    :rtype: dict(str,catkin_pkg.Package)
    """
    packages = dict()
    workspace_packages = getPackages(package_dir)

    if not workspace_packages:
        log.error(
            "Directory {} does not contain any catkin packages.".format(package_dir))

    for package_name in package_names:
        found_packages = [pkg for path, pkg in workspace_packages.items() if pkg.name == package_name]
        if not found_packages:
            log.warn("Package {} is not present in directory {}. Skipping it.".format(package_name, package_dir))
            continue
        packages[found_packages[0].name] = found_packages[0]

    return packages


def assertCyclicDependency(packages):
    """
    Check if result of topological_order has found a cyclic dependency.

    :param packages: Dict of packages.
    :type packages: dict(str, catkin_pkg.Package)
    """
    if packages:
        last_package = packages[-1]
        if not last_package[0]:
            log.error("Cyclic dependency detected. Involved packages: {}".format(last_package[1]))


def getRecursiveDownstreamDependenciesFromNames(package_names, package_dir):
    """
    Get all downstream dependencies of 'package_names' that are contained in 'package_dir'

    :param packages: List of package names.
    :type packages: list(str)
    :param package_dir: Directory in which downstream dependencies are searched.
    :type package_dir: str
    :returns: A dict of packages containing the downstream dependencies.
    :rtype: dict(str,catkin_pkg.Package)
    """
    dependencies = dict()
    workspace_packages = topological_order(package_dir)
    assertCyclicDependency(workspace_packages)

    for package_name in package_names:
        build_deps = [p for dp, p in get_recursive_build_dependents_in_workspace(package_name, workspace_packages)]
        for build_dep in build_deps:
            dependencies[build_dep.name] = build_dep

    return dependencies


def getRecursiveDownstreamDependencies(packages, package_dir):
    """
    Get all downstream dependencies of 'packages' that are contained in 'package_dir'

    :param packages: Dict of packages.
    :type packages: dict(str, catkin_pkg.Package)
    :param package_dir: Directory in which downstream dependencies are searched.
    :type package_dir: str
    :returns: A dict of packages containing the downstream dependencies.
    :rtype: dict(str,catkin_pkg.Package)
    """
    return getRecursiveDownstreamDependenciesFromNames(packages.keys(), package_dir)


# TODO(ghottiger) Using run and build depend, write wrapper for caktin_pkg to select deps.
def getRecursiveUpstreamDependencies(packages, package_dir):
    """
    Get all upstream dependencies of 'packages' that are contained in 'package_dir'

    :param packages: Dict of packages.
    :type packages: dict(str, catkin_pkg.Package)
    :param package_dir: Directory in which upstream dependencies are searched.
    :type package_dir: str
    :returns: A dictionary of packages containing the upstream dependencies.
    :rtype: dict(str,catkin_pkg.Package)
    """
    dependencies = dict()
    workspace_packages = topological_order(package_dir)
    assertCyclicDependency(workspace_packages)

    for package_name, package in packages.items():
        build_deps = [p for dp, p in get_recursive_build_depends_in_workspace(package, workspace_packages)]
        for build_dep in build_deps:
            dependencies[build_dep.name] = build_dep

    return dependencies


def getNotInstalledUpstreamDependencies(packages, package_dir, installed_package_dir):
    """
    Get upstream dependencies of 'packages' that are not installed in 'installed_package_dir'

    :param packages: Dict of packages.
    :type packages: dict(str, catkin_pkg.Package)
    :param package_dir: Directory in which upstream dependencies are searched.
    :type package_dir: str
    :param installed_package_dir: Directory in which a part of the upstream dependencies are installed.
    :type installed_package_dir: str
    :returns: A set of packages containing the upstream dependencies that are not installed
    :rtype: dict(str,catkin_pkg.Package)
    """
    workspace_upstream_dependencies = getRecursiveUpstreamDependencies(packages, package_dir)
    installed_packages = getPackages(installed_package_dir)
    dependencies = {k: workspace_upstream_dependencies[k]
                    for k in set(workspace_upstream_dependencies) - set(installed_packages)}
    return dependencies


def getFilteredPackages(packages, filter_packages, filter_packages_tree):
    """
    Filter 'packages'.

    :param packages: Dict of packages.
    :type packages: dict(str,catkin_pkg.Package)
    :param filter_packages: Packages to filter for.
    :type filter_packages: list(str)
    :param filter_packages_tree: Upstream dependencies of the filter_packages.
    :type filter_packages_tree: dict(str,catkin_pkg.Package)
    :returns: Dictionary of the filtered packages.
    :rtype: dict(str,catkin_pkg.Package)
    """

    filtered_packages_names = set(packages.keys()) & set(filter_packages_tree.keys())
    filtered_packages = dict((k, packages[k]) for k in filtered_packages_names)
    for pkg in filter_packages:
        if pkg in packages.keys():
            filtered_packages[pkg] = packages[pkg]
    return filtered_packages


############################
### Template utils       ###
############################

def updateFileFromTemplate(template_file, output_file, substitutions):
    """
    Filter 'packages' for the

    :param template_file: Path of the template file.
    :type template_file: str
    :param output_file: Path of the output file.
    :type output_file: str
    :param substitutions: Substitutions to apply.
    :type substitutions: dict(str,str)
    """

    # Expand template
    with open(template_file, 'r') as fh:
        result = em.expand(fh.read(), **substitutions)

    # Write the result
    with open(output_file, 'w+') as f:
        content = f.read()
        if content != result:
            f.write(result)
