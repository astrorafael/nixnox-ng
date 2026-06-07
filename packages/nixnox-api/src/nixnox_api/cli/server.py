# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import logging
from argparse import ArgumentParser, Namespace

from typing import Any

# ---------------------------
# Third-party library imports
# ----------------------------

import decouple
import uvicorn
from lica.cli import execute

# --------------
# local imports
# -------------

from nixnox_api import __version__
from ..fastapi import app as app

# get the module logger
log = logging.getLogger("http")

DESCRIPTION = "NIXNOX HTTP API Server"

# -------------------
# Auxiliary functions
# -------------------


def cli_main(args: Namespace) -> None:
    env_host = decouple.config("HTTP_LISTEN_ADDR", default="localhost")
    env_port = decouple.config("HTTP_PORT", cast=int, default=8086)
    host = args.host or env_host
    port = args.port or env_port
    log.info("Starting NIXNOX HTTP Server on %s:%d", host, port)
    config = uvicorn.Config(
        f"{__name__}:app",
        host=host,
        port=port,
        log_level="error",
        use_colors=False,
    )
    server = uvicorn.Server(config)
    server.run()  # Start a bg blocking thread and manage the API


def add_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-ho",
        "--host",
        type=str,
        default=None,
        help="HTTP server host address(default %(default)s)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=None,
        help="HTTP server TCP port(default %(default)s)",
    )


def main():
    """The main entry point specified by pyproject.toml"""
    execute(
        main_func=cli_main,
        add_args_func=add_args,
        name=__name__,
        version=__version__,
        description=DESCRIPTION,
    )


if __name__ == "__main__":
    main()
