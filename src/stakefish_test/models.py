from typing import Optional

from dns import rdatatype, resolver
from pydantic import BaseModel
from pydantic.networks import IPv4Address


class Address(BaseModel):
    id: Optional[str]
    ip: IPv4Address


class Query(BaseModel):
    id: str
    addresses: list[Address]
    client_ip: str
    created_at: int
    domain: str

    def resolve(self) -> list[Address]:
        answer = resolver.resolve(qname=self.domain, rdtype=rdatatype.A)

        self.addresses = [
            Address(id="", ip=IPv4Address(ip_addr))
            for ip_addr in answer.rrset.items.keys()
        ]
