# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import logging
import secrets

from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone

# -------------------
# Third party imports
# -------------------


from lica.sqlalchemy import sqa_logging
from lica.sqlalchemy.noasync.dbase import create_engine_sessionclass
from lica.cli import execute

# --------------
# local imports
# -------------

from nixnox_dao import __version__
from nixnox_dao.auth.noasync import User
from nixnox_dao.auth.utils import hash_password
from nixnox_dao.auth.constants import AuthRole

# ----------------
# Module constants
# ----------------

DESCRIPTION = "NIXNOX Database initial populate tool"

# -----------------------
# Module global variables
# -----------------------


# get the module/package logger

log = logging.getLogger(__name__.split(".")[-1])

# get the database engine and session factory object
engine, Session = create_engine_sessionclass(env_var="AUTH_DB_URL")

# -------------------
# Auxiliary functions
# -------------------


# -------------
# CLI Functions
# -------------


def cli_populate_user(session: Session, args: Namespace) -> None:
    log.info("Generating default Admin user")
    user = User(
        username="admin",
        password_hash=hash_password(args.password),
        full_name="Admin User",
        role=AuthRole.ADMIN,
        api_key=secrets.token_urlsafe(32),
        created_at=datetime.now(timezone.utc).replace(microsecond=0),
    )
    with session.begin():
        session.add(user)


def add_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        default="1234",
        help="Admin password (default %(default)s)",
    )

    parser.set_defaults(func=cli_populate_user)


def cli_main(args: Namespace) -> None:
    sqa_logging(args)
    with Session() as session:
        args.func(session, args)
    engine.dispose()


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
