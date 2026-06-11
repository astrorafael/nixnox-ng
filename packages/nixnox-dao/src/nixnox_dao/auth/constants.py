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

# column lengths

LOGIN_LEN = 32
HASH_LEN = 512
NAME_LEN = 255
APIKEY_LEN = 43  # 32 bytes encoded in base64 → ~43 chars


# Authentication Roles


class AuthRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
