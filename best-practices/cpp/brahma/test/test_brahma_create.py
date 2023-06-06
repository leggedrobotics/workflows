#!/usr/bin/python3

from pathlib import Path

import brahma.brahma_create as brahma_create
from .conftest import BrahmaTestWorkspace


def test_basic(brahma_ws_with_repo: BrahmaTestWorkspace) -> None:
    brahma_ws_with_repo.set_default_create_args()
    brahma_create.run(paths=brahma_ws_with_repo.paths, settings=brahma_ws_with_repo.settings,
                      args=brahma_ws_with_repo.args)
    # Check that directories created by 'brahma create' exist.
    assert Path(brahma_ws_with_repo.paths.source).exists()
    assert Path(brahma_ws_with_repo.paths.catkinSource()).exists()
    assert (Path(brahma_ws_with_repo.paths.source) / "repo").exists()
