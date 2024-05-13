import importlib.metadata
from pathlib import Path

import toml


def get_version(package_name: str):
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        pyproject_toml_file = Path(__file__).parent.parent.parent / "pyproject.toml"
        if not (pyproject_toml_file.exists() or pyproject_toml_file.is_file()):
            return "unknown"

        data = toml.load(pyproject_toml_file)
        if "project" in data and "version" in data["project"]:
            return data["project"]["version"]

        return "undefined"
