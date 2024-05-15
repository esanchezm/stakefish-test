from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

from .database import get_session
from .models import Query


def create_query(query: Query, db: Session = Depends(get_session)):
    query_to_db = Query.model_validate(query)

    db.add(query_to_db)
    db.commit()
    db.refresh(query_to_db)

    return query_to_db


def get_queries_history(limit: int = 20, db: Session = Depends(get_session)):
    queries = db.exec(
        select(Query).order_by(Query.created_at.desc()).limit(limit)
    ).all()

    return queries


def count_queries_per_domain(db: Session):
    """
    Get count of queries per domain
    """
    return db.exec(
        select(Query.domain, func.count(Query.domain)).group_by(Query.domain)
    ).all()
