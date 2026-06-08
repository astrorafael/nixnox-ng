# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

from typing import Annotated

# ---------------------
# Third party libraries
# ---------------------


from pydantic import BaseModel, AfterValidator, EmailStr, HttpUrl

from nixnox_dao import NICK_LEN, NAME_LEN

PASSWD_LEN = 32
ACRONYM_LEN = 8

# --------------------
# Pydantic annotations
# --------------------

NickName = Annotated[str, AfterValidator(lambda v: len(v) <= NICK_LEN)]
FullName = Annotated[str, AfterValidator(lambda v: len(v) <= NAME_LEN)]
Password = Annotated[str, AfterValidator(lambda v: len(v) <= PASSWD_LEN)]
Acronym = Annotated[str, AfterValidator(lambda v: len(v) <= ACRONYM_LEN)]


# ---------------
# Pydantic Models
# ---------------


class PersonCreate(BaseModel):
    nick: NickName
    fullname: FullName
    password: Password


class OrganizantionCreate(BaseModel):
    nick: NickName
    password: Password
    fullname: FullName
    acronym: Acronym
    website: HttpUrl
    email: EmailStr

