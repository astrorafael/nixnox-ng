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
from nixnox_dao.auth.constants import TOKEN_LEN
from .util import parser as prs

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
    log.info("Creating user %s", args.login)
    with session.begin():
        user = session.scalars(select(User).where(User.login == args.login)).one_or_none()
        if user is not None:
            raise KeyError(f"User {args.login} already exists")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    user = User(
        login=args.login,
        password_hash=hash_password(args.password),
        role=args.role,
        api_key=secrets.token_urlsafe(TOKEN_LEN),  # 32 bytes base64 encoded => 43 bytes approx.
        created_at=now,
        updated_at=now,
    )
    with session.begin():
        session.add(user)


def cli_delete_user(session: Session, args: Namespace, log: Logger = log) -> None:
    log.info("Deleting user %s", args.login)
    with session.begin():
        user = session.scalars(select(User).where(User.login == args.login)).one_or_none()
        if user is None:
            raise KeyError(f"User {args.login} does not exists")
        session.delete(user)


def cli_update_user(session: Session, args: Namespace, log: Logger = log) -> None:
    log.info("Updating user %s", args.login)
    with session.begin():
        user = session.scalars(select(User).where(User.login == args.login)).one_or_none()
        if user is None:
            raise KeyError(f"User {args.login} does not exists")
        changed = False
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


def cli_list_user(session: Session, args: Namespace, log: Logger = log) -> None:
    with session.begin():
        if args.login is not None:
            log.info("Listing user %s", args.login)
            q = select(User).where(User.login == args.login)
            user = session.scalars(q).one_or_none()
            if user is None:
                log.info("User %s not found", args.login)
            else:
                log.info("%s", user)
        else:
            q = select(User)
            users = session.scalars(q).all()
            for user in users:
                log.info("%s", user)
            log.info("Listing all users")


def add_args(parser: ArgumentParser) -> None:
    subparser = parser.add_subparsers(dest="command", required=True)
    p = subparser.add_parser(
        "create",
        parents=[prs.login(), prs.passwd(), prs.role()],
        help="Create a new user",
    )
    p.set_defaults(func=cli_create_user)
    p = subparser.add_parser(
        "update",
        parents=[prs.login(), prs.passwd(), prs.role(), prs.apk()],
        help="Update user attributes",
    )
    p.set_defaults(func=cli_update_user)
    p = subparser.add_parser(
        "delete",
        parents=[prs.login()],
        help="Delete user",
    )
    p.set_defaults(func=cli_delete_user)
    p = subparser.add_parser("list", parents=[prs.login(required=False)], help="Delete user")
    p.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Regenerate API Key",
    )
    p.set_defaults(func=cli_list_user)


def cli_main(args: Namespace) -> None:
    sqa_logging(args)
    with Session() as session:
        args.func(session, args, log=log)
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
