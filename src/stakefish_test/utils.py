import importlib.metadata
from ipaddress import AddressValueError
from pathlib import Path

import toml
from pydantic import BaseModel, Field
from pydantic.networks import IPv4Address


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


class QueryRequest(BaseModel):
    domain: str = Field(examples=["cloudflare.com"])


class ValidateIPRequest(BaseModel):
    ip: str = Field(examples=["192.168.5.4"])

    def is_valid(self) -> bool:
        try:
            IPv4Address(self.ip)
        except AddressValueError:
            return False
        return True


class ValidateIPResponse(BaseModel):
    valid: bool
