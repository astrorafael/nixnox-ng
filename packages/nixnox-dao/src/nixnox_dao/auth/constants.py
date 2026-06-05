# ----------------------------------------------------------------------
# Copyright (c) 2022
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------


from enum import StrEnum


# Authentication Roles


class AuthRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
