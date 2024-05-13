import os
import time

import utils
from fastapi import FastAPI

VERSION = utils.get_version("stakefish-test")

def get_application():
    app = FastAPI(
        title='Interview challenge',
        description='Implementation for the interview challenge',
        debug="DEBUG" in os.environ,
        version=VERSION,
    )


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
    return {
        "status": "up",
    }
