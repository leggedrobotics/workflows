#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import os
import sys

import brahma.log as log

try:
    import git
    from git import RemoteProgress
    from git import Repo
except:
    log.error(
        "The current directory does not exist in the base branch. Try to run the command from the root of your brahma workspace.")


class GitProgressPrinter(RemoteProgress):
    """
    Progress printer for GitPython cloning. See GitPython documentation for details.
    """

    def update(self, op_code, cur_count, max_count=None, message=''):
        OP_NAMES = {
            RemoteProgress.BEGIN: 'Begin',
            RemoteProgress.CHECKING_OUT: 'Checkout',
            RemoteProgress.COMPRESSING: 'Compressing',
            RemoteProgress.COUNTING: 'Counting',
            RemoteProgress.END: 'End',
            RemoteProgress.FINDING_SOURCES: 'Finding Sources',
            RemoteProgress.OP_MASK: 'OP Mask',
            RemoteProgress.RECEIVING: 'Receiving',
            RemoteProgress.RESOLVING: 'Resolving',
            RemoteProgress.STAGE_MASK: 'Stage mask',
            RemoteProgress.WRITING: 'Writing'
        }
        if op_code in OP_NAMES:
            print("\033[K", end='\r')
            print(OP_NAMES[op_code] + " {0:.1f}%".format(100.0 * cur_count / (max_count or 100.0)), end='\r')


def cloneRepository(url, dir):
    """
    Clone repository into directory.

    :param url: URL of the repository
    :type url: str
    :param dir: Directory in which to clone repository.
    :type dir: str
    """
    if os.path.exists(dir):
        log.error("Tried to clone repo into existing folder {}".format(dir))
    try:
        Repo.clone_from(url, dir, progress=GitProgressPrinter())
        log.info("")  # Line break
    except git.exc.GitCommandError:
        log.error("Could not clone repo from {}".format(url))


def cloneOrLinkRepositories(repositories, dir):
    """
    Clone or symlink repositories into directory and check out the base branch.

    :param repositories: Repository information
    :type repositories: dict(str, pair(str,str))
    :param dir: Directory in which to clone repository.
    :type dir: str
    """
    for repo_name, repo_info in repositories.items():
        repo_url = repo_info[0]
        repo_base_branch = repo_info[1]
        repo_path = dir + "/" + repo_name
        if not os.path.exists(repo_path):
            if repo_url.endswith(".git"):  # Can be local or remote repo
                log.prefixStatus("Cloning repository '{}' with URL".format(repo_name), '{}'.format(repo_url))
                log.prefixStatus('into path', '{}'.format(repo_path))
                cloneRepository(repo_url, repo_path)
            elif os.path.exists(repo_url):
                log.prefixStatus("Symlinking repository '{}' with path".format(repo_name), '{}'.format(repo_url))
                log.prefixStatus('into path', '{}'.format(repo_path))
                os.symlink(repo_url, repo_path)
            else:
                log.warn("Repository '{}' with URL {} is not valid. Skip creation.".format(repo_name, repo_url))
                continue
            # Check out the base branch
            git_repo = getRepository(repo_path)
            log.prefixStatus('Check out base branch', '{}'.format(repo_base_branch))
            checkoutBranch(git_repo, repo_base_branch, pull=False, abortOnError=False)
        else:
            log.info("Existing repository in folder '{}'".format(repo_path))


def isGitRepo(path):
    """
    Check if 'path' is a git directory

    :param path: Path to check
    :type path: str
    :returns: True, if 'path' is a repository
    :rtype: bool
    """
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def getRepository(dir):
    """
    Get repository at path. Exit process if non-existing folder.

    :returns: Repository at 'dir'
    :rtype: git.Repo
    """
    if not os.path.exists(dir):
        log.error("Tried to init repo from non-existing folder {}".format(dir))
    return Repo(dir)


def getRepositories(git_dir):
    """
    Get repository at path. Exit process if non-existing folder.

    :param git_dir: Directory containing the git repositories
    :type git_dir: str
    :returns: List of repository in 'git_dir'
    :rtype: list of git.Repo
    """
    repos = list()
    for dir, subdirs, files in os.walk(git_dir, followlinks=True):
        if isGitRepo(dir):
            repos.append(dir)
            del subdirs[:]
    return repos


def getRepoNameFromURL(url):
    """
    Get repository name from the URL.

    :param url: Repository url
    :type url: str
    :returns: Extracted repository name
    :rtype: str
    """
    last_slash_index = url.rfind("/")
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1:last_suffix_index]


def getURLFromRepoPath(path):
    """
    Get repository URL from repository at 'path'.

    :param path: Repository path
    :type path: str
    :returns: Extracted repository url, 'None' if not a git repository
    :rtype: str
    """
    if isGitRepo(path):
        return git.Repo(path).remotes.origin.url
    return None


def createBranch(repo, branch_name):
    """
    Create a new branch with name 'branch_name' for 'repo'

    :param repo: Repository
    :type repo: git.Repo
    :param branch_name: Name of the created branch
    :type branch_name: str
    """
    try:
        repo.git.checkout('-b', branch_name)
    except git.exc.GitCommandError:
        log.error("Could not checkout new branch {}".format(branch_name))


def pullBranch(repo, branch_name):
    """
    Pull branch 'branch_name' for 'repo'

    :param repo: Repository
    :type repo: git.Repo
    :param branch_name: Name of the branch to checkout
    :type branch_name: str
    """
    repo.remotes.origin.fetch(branch_name + ":" + branch_name, progress=GitProgressPrinter())


def checkoutBranch(repo, branch_name, pull, abortOnError=True):
    """
    Checkout and update branch 'branch_name' for 'repo'

    :param repo: Repository
    :type repo: git.Repo
    :param branch_name: Name of the branch to checkout
    :type branch_name: str
    :param pull: If true pull the branch from origin after checkout
    :type pull: bool
    :param abortOnError: Abort if branch can not be checked out
    :type abortOnError: bool
    """
    repo.remotes.origin.fetch()

    try:
        output = repo.git.checkout(branch_name)
    except git.exc.GitCommandError:
        if abortOnError:
            log.error("Could not checkout branch {}".format(branch_name))
        else:
            log.warn("Could not checkout branch {}. Continue with current branch.".format(branch_name))
            return ''

    if pull:
        try:
            repo.remotes.origin.pull()
        except git.exc.GitCommandError:
            log.warn("Could not pull branch {}. Continue with local state.".format(branch_name))
    return output


def mergeBranch(repo, branch_name):
    try:
        return repo.git.merge(branch_name)
    except git.exc.GitCommandError:
        log.error("Could not merge branch {}. Please resolve conflicts, local remain were stashed.".format(branch_name))


def stashChanges(repo, stash_name):
    try:
        return repo.git.stash('save', '-u', stash_name)
    except git.exc.GitCommandError:
        log.error("Could not stash changes")


def popStash(repo):
    try:
        return repo.git.stash('pop')
    except git.exc.GitCommandError:
        log.error("Could not pop stash, changes remain stashed.")


def hasStash(stash_return_string, stash_name):
    return stash_return_string.find(stash_name) != -1
