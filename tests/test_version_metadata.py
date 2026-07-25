import tomllib
from importlib.metadata import metadata, version
from pathlib import Path

import gmshparser


def _project_metadata():
    with Path("pyproject.toml").open("rb") as project_file:
        return tomllib.load(project_file)["project"]


def test_runtime_version_matches_project_metadata():
    project = _project_metadata()

    assert version("gmshparser") == project["version"]
    assert gmshparser.__version__ == project["version"]


def test_distribution_metadata_declares_supported_python_and_typing():
    project = _project_metadata()
    distribution = metadata("gmshparser")

    assert distribution["Requires-Python"] == project["requires-python"]
    assert "Typing :: Typed" in distribution.get_all("Classifier", [])
    assert "gmsh" in project["keywords"]
