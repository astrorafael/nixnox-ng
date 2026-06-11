# ----------------------------------------------------------------------
# Copyright (c) 2022
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# ----------------
# standard imports
# ----------------

import re
import hashlib
from typing import Annotated, Optional

# ---------------------
# Third party libraries
# ---------------------

from pydantic import (
    BaseModel,
    ValidationError,
    AfterValidator,
)
from nixnox_dao import AuthRole, NAME_LEN, NICK_LEN, APIKEY_LEN

# ---------
# Constants
# ---------

PASSWD_LEN = 32

# ------------------
# Auxiliar functions
# ------------------


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica contraseña contra hash almacenado."""
    salt, stored_hash = password_hash.split("$")
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return new_hash == stored_hash


# --------------------
# Pydantic annotations
# --------------------


def v_nick(v: str) -> str:
    pattern = r"^[a-zA-Z0-9_]{3," + str(NICK_LEN) + r"}$"
    if not re.match(pattern, v):
        raise ValueError(f"nickname must be alphanumeric or _ and between 3-{NAME_LEN} chars long")
    return v.strip().lower()


def v_api_key(v: str) -> str:
    """Validate API key generated with secrets.token_urlsafe(32)"""

    # base64 encoding: [A-Za-z0-9_-]
    pattern = r"^[A-Za-z0-9_-]{" + str(APIKEY_LEN) + r"}$"
    if not re.match(pattern, v):
        raise ValueError(f"API key inválida must be {APIKEY_LEN} URL-safe (A-Za-z0-9_-) chars long")
    return v


def v_fullname(v: str) -> str:
    if len(v) > NAME_LEN:
        raise ValidationError(f"full name too long: {len(v)} > {NAME_LEN}")
    return v


def v_password(v: str) -> str:
    if len(v) > PASSWD_LEN:
        raise ValidationError(f"password too long: {len(v)} > {PASSWD_LEN}")
    return v


# --------------------
# Pydantic annotations
# --------------------

NickName = Annotated[str, AfterValidator(v_nick)]
FullName = Annotated[str, AfterValidator(v_fullname)]
Password = Annotated[str, AfterValidator(v_password)]
ApiKey = Annotated[str, AfterValidator(v_api_key)]


class UserCreateInfo(BaseModel):
    login: NickName
    password: Password
    full_name: FullName
    role: AuthRole


class UserModifyInfo(BaseModel):
    login: NickName
    password: Optional[Password] = None
    full_name: Optional[FullName] = None
    role: Optional[AuthRole] = None
    api_key: bool = False  # generate new api key ?


class UserDeleteInfo(BaseModel):
    login: NickName


class UserAuthenticateInfo(BaseModel):
    login: NickName
    password: Password


class UserLookupApiKey(BaseModel):
    apikey: ApiKey
