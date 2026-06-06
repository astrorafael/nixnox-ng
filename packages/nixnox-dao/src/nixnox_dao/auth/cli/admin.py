# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import logging
from logging import Logger
import secrets

from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone

# -------------------
# Third party imports
# -------------------

from sqlalchemy import select

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

DESCRIPTION = "NIXNOX Auth Database admin tool"

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


def cli_create_user(session: Session, args: Namespace, log: Logger = log) -> None:
    log.info("Creating user %s", args.username)
    with session.begin():
        user = session.execute(
            select(User).where(User.username == args.username)
        ).scalar_one_or_none()
        if user is not None:
            raise KeyError(f"User {args.username} already exists")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    user = User(
        username=args.username,
        password_hash=hash_password(args.password),
        full_name=args.fullname,
        role=AuthRole.USER,
        api_key=secrets.token_urlsafe(32),
        created_at=now,
        updated_at=now,
    )
    with session.begin():
        session.add(user)


def cli_delete_user(session: Session, args: Namespace, log: Logger = log) -> None:
    log.info("Deleting user %s", args.username)
    with session.begin():
        user = session.execute(
            select(User).where(User.username == args.username)
        ).scalar_one_or_none()
        if user is None:
            raise KeyError(f"User {args.username} does not exists")
        session.delete(user)


def cli_update_user(session: Session, args: Namespace, log: Logger = log) -> None:
    log.info("Updating user %s", args.username)
    with session.begin():
        user = session.execute(
            select(User).where(User.username == args.username)
        ).scalar_one_or_none()
        if user is None:
            raise KeyError(f"User {args.username} does not exists")
        changed = False
        if args.full_name is not None:
            user.full_name = args.full_name
            changed = True
        if args.password is not None:
            user.password_hash = hash_password(args.password)
            changed = True
        if args.api_key:
            user.api_key = secrets.token_urlsafe(32)
            changed = True
        if args.role is not None and args.role != user.role:
            user.role = args.role
            changed = True
        if changed:
            user.updated_at = datetime.now(timezone.utc).replace(microsecond=0)


def add_args(parser: ArgumentParser) -> None:
    subparser = parser.add_subparsers(dest="command", required=True)
    p = subparser.add_parser("create", parents=[], help="Create a new user")
    p.set_defaults(func=cli_create_user)
    p = subparser.add_parser("update", parents=[], help="Update user attributes")
    p.set_defaults(func=cli_update_user)
    p = subparser.add_parser("delete", parents=[], help="Delete user")
    p.set_defaults(func=cli_delete_user)


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
