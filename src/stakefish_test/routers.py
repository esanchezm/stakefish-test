import time

from fastapi import APIRouter, Request, status
from models import Query
from utils import QueryRequest, ValidateIPRequest, ValidateIPResponse

tools_router = APIRouter(
    prefix="/tools",
    tags=["tools"],
)


@tools_router.post("/lookup")
async def lookup_domain(queryRequest: QueryRequest, request: Request, db: Session = Depends(get_session)) -> Query:
    """
    Lookup domain and return all IPv4 addresses
    """
    query = Query(
        addresses=[],
        client_ip=request.client.host,
        domain=queryRequest.domain,
    )

    query.resolve()
    query = create_query(query, db)

    return query


@tools_router.post(
    "/validate",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}},
)
async def validate_ip(request: ValidateIPRequest) -> ValidateIPResponse:
    """
    Simple IP validation
    """
    return ValidateIPResponse(valid=request.is_valid())


history_router = APIRouter(
    prefix="",
    tags=["history"],
)


@history_router.get("/history", response_model=None)
def queries_history() -> None:
    """
    List queries
    """
    pass
