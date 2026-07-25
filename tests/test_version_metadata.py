import tomllib
from importlib.metadata import version
from pathlib import Path

import gmshparser


def test_runtime_version_matches_project_metadata():
    with Path("pyproject.toml").open("rb") as project_file:
        project_version = tomllib.load(project_file)["project"]["version"]

    assert version("gmshparser") == project_version
    assert gmshparser.__version__ == project_version
