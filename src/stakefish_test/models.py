from pydantic import BaseModel
from pydantic.networks import IPv4Address


class Address(BaseModel):
    id: str
    ip: IPv4Address


class Query(BaseModel):
    id: str
    addresses: list[Address]
    client_ip: str
    created_at: int
    domain: str
