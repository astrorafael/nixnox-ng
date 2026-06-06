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


def uname() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)

    return parser


def role() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)

    return parser


def passwd() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)

    return parser


def full() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)

    return parser
