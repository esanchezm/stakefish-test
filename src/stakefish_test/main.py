import os
import time

import utils
from fastapi import FastAPI

VERSION = utils.get_version("stakefish-test")

app = FastAPI()


@app.get("/")
def root():
    return {
        "version": VERSION,
        "date": time.time(),
        "kubernetes": "KUBERNETES_SERVICE_HOST" in os.environ,
    }
