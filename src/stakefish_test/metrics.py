from typing import Callable

from prometheus_client import Gauge
from prometheus_fastapi_instrumentator.metrics import Info
from sqlmodel import Session

from .crud import count_queries_per_domain
from .database import engine


def queries_total() -> Callable[[Info], None]:
    METRIC = Gauge(
        "queries_total", "Number of total queries per domain.", labelnames=("domain",)
    )

    def instrumentation(info: Info) -> None:
        session = Session(engine)
        data = count_queries_per_domain(db=session)
        session.close()
        for domain in data:
            METRIC.labels(domain[0]).set(domain[1])

    return instrumentation
