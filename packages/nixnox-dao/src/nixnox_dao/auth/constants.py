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

# -------------
# local imports
# -------------

from nixnox_dao.nixnox.constants import NICK_LEN as LOGIN_LEN  # noqa: F401

# additional column lengths

HASH_LEN = 512
TOKEN_LEN = 32
APIKEY_LEN = 43  # 32 bytes encoded in base64 → ~43 chars


# Authentication Roles


class AuthRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
