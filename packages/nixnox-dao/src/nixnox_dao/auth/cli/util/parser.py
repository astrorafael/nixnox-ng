# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

from argparse import ArgumentParser

# ---------------------------
# Third-party library imports
# ----------------------------


# --------------
# local imports
# -------------

from nixnox_dao import AuthRole


def login(required=True) -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-l",
        "--login",
        type=str,
        required=required,
        default=None,  # only when required is False
        help="log-in username",
    )
    return parser


def passwd() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        default=None,
        help="User password",
    )
    return parser


def role() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-r",
        "--role",
        type=AuthRole,
        default=AuthRole.USER,
        help="User role (default %(default)s)",
    )
    return parser


def full() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-f",
        "--full-name",
        type=str,
        default=None,
        help="User full name without spaces, quote or use _ instead (default %(default)s)",
    )
    return parser


def apk() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-k",
        "--api-key",
        action="store_true",
        default=False,
        help="Regenerate API Key",
    )
    return parser
