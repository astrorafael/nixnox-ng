# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

from typing import Type

# ---------------------
# Third party libraries
# ---------------------

from lica.sqlalchemy.asyncio.model import Model

# -------------------
# Own package imports
# -------------------

from nixnox_dao.auth.model import make_User


# Tables creation with the no async Model behaviour built-in


# Authentication Data Access Object
User: Type = make_User(Model)


__all__ = [
    "User",
]
