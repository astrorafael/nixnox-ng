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
from datetime import datetime, timezone
from typing import Annotated, Optional, Union

# ---------------------
# Third party libraries
# ---------------------

from pydantic import (
    BaseModel,
    ValidationError,
    BeforeValidator,
    AfterValidator,
    HttpUrl,
)
from nixnox_dao import AuthRole, NAME_LEN, NICK_LEN, APIKEY_LEN

# ---------
# Constants
# ---------

PASSWD_LEN = 32
ACRONYM_LEN = 8

# Sequence of possible timestamp formats
TSTAMP_FORMAT = (
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d %H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S%z",  # timezone aware that must be converted to UTC
    "%Y-%m-%d %H:%M:%S%z",  # timezone aware that must be converted to UTC
)

# ------------------
# Auxiliar functions
# ------------------


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

def v_acronym(v: str) -> str:
    pattern = r"^[a-zA-Z0-9_.]{2," + str(ACRONYM_LEN) + r"}$"
    if not re.match(pattern, v):
        raise ValueError(f"acronym must be alphanumeric or _ and . and between 2-{NAME_LEN} chars long")
    return v.strip().lower()

def v_datetime(value: Union[str, datetime, None]) -> datetime:
    if value is None:
        return (datetime.now(timezone.utc) + timedelta(seconds=0.5)).replace(microsecond=0)
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise ValidationError("tstamp must be a string or datetime.")
    for i, fmt in enumerate(TSTAMP_FORMAT):
        try:
            if i < 4:
                return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
            else:
                return datetime.strptime(value, fmt).astimezone(timezone.utc)
        except ValueError:
            continue
    raise ValidationError(f"{value} tstamp must be in one of {TSTAMP_FORMAT} formats.")

# --------------------
# Pydantic annotations
# --------------------

NickName = Annotated[str, AfterValidator(v_nick)]
FullName = Annotated[str, AfterValidator(v_fullname)]
Password = Annotated[str, AfterValidator(v_password)]
ApiKey = Annotated[str, AfterValidator(v_api_key)]
Acronym = Annotated[str, AfterValidator(v_acronym)]
DateTime = Annotated[Union[str, datetime, None], BeforeValidator(v_datetime)]


class ObserverCreateReq(BaseModel):
    nickname: NickName
    password: Password
    role: AuthRole

class PersonCreateReq(ObserverCreateReq):
    full_name: FullName


class OrganizantionCreateReq(ObserverCreateReq):
    full_name: FullName
    acronym: Acronym
    website: HttpUrl


class ObserverModifyReq(BaseModel):
    nickname: NickName
    password: Optional[Password] = None
    full_name: Optional[FullName] = None
    role: Optional[AuthRole] = None
    new_api_key: bool = False  # generate new api key ?


class ObserverDeleteReq(BaseModel):
    login: NickName


class ObserverAuthenticateReq(BaseModel):
    login: NickName
    password: Password
