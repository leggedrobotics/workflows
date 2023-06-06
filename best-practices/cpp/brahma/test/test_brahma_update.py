#!/usr/bin/python3

from pathlib import Path

import brahma.brahma_create as brahma_create
import brahma.brahma_update as brahma_update
from testing_infrastructure.repositories.Repository import Repository
from testing_infrastructure.utils import commit_default_package
from .conftest import BrahmaTestWorkspace


def test_basic(brahma_ws_with_repo: BrahmaTestWorkspace) -> None:
    # Create a default brahma workspace.
    brahma_ws_with_repo.set_default_create_args()
    brahma_create.run(paths=brahma_ws_with_repo.paths, settings=brahma_ws_with_repo.settings,
                      args=brahma_ws_with_repo.args)

    # Add a package to the master branch.
    repo = Repository(name="repo", path=Path(brahma_ws_with_repo.paths.source))
    assert (repo.git_repo is not None)
    commit_default_package(repo=repo, name="package_a")

    # Check out a new branch and update the brahma workspace.
    repo.checkout(ref="test/package_diff", new=True)
    brahma_ws_with_repo.set_default_update_args()
    brahma_update.run(paths=brahma_ws_with_repo.paths, settings=brahma_ws_with_repo.settings,
                      args=brahma_ws_with_repo.args)
    # Ensure that the package was not added to the catkin workspace.
    assert not (Path(brahma_ws_with_repo.paths.catkinSource()) / "package_a").exists()

    # Commit a new file in the package and update the brahma workspace once more.
    repo.commit_new(rel_path=Path("package_a") / "trigger_update")
    brahma_update.run(paths=brahma_ws_with_repo.paths, settings=brahma_ws_with_repo.settings,
                      args=brahma_ws_with_repo.args)
    # Ensure that the package was added to the catkin workspace.
    assert (Path(brahma_ws_with_repo.paths.catkinSource()) / "package_a").exists()
