import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import database, routers, utils

VERSION = utils.get_version("stakefish-test")


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield
    database.engine.dispose()


def get_application():
    app = FastAPI(
        title="Interview challenge",
        description="Implementation for the interview challenge",
        debug="DEBUG" in os.environ,
        version=VERSION,
        lifespan=lifespan,
    )

    app.include_router(routers.tools_router)
    app.include_router(routers.history_router)

    return app


app = get_application()


@app.get("/")
def root():
    """
    Return basic version information
    """
    return {
        "version": VERSION,
        "date": time.time(),
        "kubernetes": "KUBERNETES_SERVICE_HOST" in os.environ,
    }


@app.get("/health")
def health():
    """
    Return health status
    """
    # This could be improved by checking the database connection
    # but based on my experience it's better to have it in the readiness probe
    # Since this application has no external dependencies, it's fine to return "up"
    return {
        "status": "up",
    }
