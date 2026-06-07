# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import logging

# ---------------------------
# Third-party library imports
# ----------------------------

from fastapi import FastAPI


# ----------------
# Global variables
# ----------------

log = logging.getLogger("http")
app = FastAPI()

# ==============================
# HTTP Generic FastAPI Endpoints
# ==============================


@app.get("/v1")
async def root():
    log.info("Received hello request")
    return {"message": "I'm alive"}


__all__ = [
    "app",
]
