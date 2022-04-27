import argparse
from pathlib import Path
import pytest
from typing import List

import brahma.BrahmaWorkspacePaths as BrahmaWorkspacePaths
import brahma.BrahmaWorkspaceSettings as BrahmaWorkspaceSettings
from testing_infrastructure.repositories.LocalRemote import LocalRemote
from testing_infrastructure.repositories import Repository


class BrahmaTestWorkspace:
    """
    Test helper object that stores settings of the brahma workspace to be tested.
    """
    __slots__ = ["args", "repositories", "paths", "settings"]

    def __init__(self, paths: BrahmaWorkspacePaths, settings: BrahmaWorkspaceSettings):
        self.args = argparse.Namespace()
        self.paths = paths
        self.settings = settings
        self.repositories: List[List[str]] = []

    def path(self) -> Path:
        """
        Get path of the workspace as a pathlib object.
        """
        return Path(self.paths.workspace)

    def add_repository(self, repository: List[str]) -> None:
        """
        Add a repository to the arguments list (brahma create -r/--repository option).
        """
        self.repositories.append(repository)

    def set_default_create_args(self) -> None:
        """
        Populate arguments list with defaults for creation. Add registered repositories.
        """
        self.args = argparse.Namespace()
        self.args.config = "default"
        self.args.force = False
        self.args.repository = self.repositories

    def set_default_update_args(self) -> None:
        """
        Populate arguments list with defaults for the update step.
        """
        self.args = argparse.Namespace()
        self.args.pull = False
        self.args.pull_and_merge = False


def default_brahma_ws(path: Path) -> BrahmaTestWorkspace:
    """
    Returns a default brahma test workspace object.
    """
    settings = BrahmaWorkspaceSettings.BrahmaWorkspaceSettings()
    paths = BrahmaWorkspacePaths.BrahmaWorkspacePaths(str(path / 'brahma_ws'))
    return BrahmaTestWorkspace(paths=paths, settings=settings)


@pytest.fixture
def brahma_ws(tmp_path: Path) -> BrahmaTestWorkspace:
    """
    Fixture setting up a default brahma test workspace object.
    """
    return default_brahma_ws(tmp_path)


@pytest.fixture
def brahma_ws_with_repo(brahma_ws: BrahmaTestWorkspace) -> BrahmaTestWorkspace:
    """
    Fixture setting up a default brahma test workspace object and a single "local" remote repository to pull from.
    """
    local_remote = LocalRemote(name='repo', path=Path(brahma_ws.path().parent))
    brahma_ws.add_repository([local_remote.name, str(local_remote.url), "master"])
    return brahma_ws
