from datetime import datetime
from typing import Optional

import sqlalchemy
from dns import exception, rdatatype, resolver
from pydantic.networks import IPv4Address
from sqlmodel import Field, Relationship, SQLModel

from .utils import IPv4AddresssType


class AddressBase(SQLModel):
    ip: IPv4Address = Field(nullable=False, sa_type=IPv4AddresssType)


class Address(AddressBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    query_id: int | None = Field(default=None, foreign_key="query.id")
    query: Optional["Query"] = Relationship(back_populates="addresses")  # type: ignore


class AddressOutput(AddressBase):
    pass


class QueryBase(SQLModel):
    client_ip: IPv4Address = Field(sa_type=IPv4AddresssType)
    domain: str


class Query(QueryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
    addresses: list[Address] = Relationship(back_populates="query")

    def resolve(self):
        try:
            answer = resolver.resolve(qname=self.domain, rdtype=rdatatype.A)
        except exception.DNSException:
            return []

        self.addresses = [
            Address(ip=IPv4Address(ip_addr)) for ip_addr in answer.rrset.items.keys()
        ]


class QueryOutput(QueryBase):
    id: int
    domain: str
    created_at: datetime
    addresses: list[AddressOutput]
