# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

from datetime import datetime, timezone, timedelta
from typing import Annotated, Union

# ---------------------
# Third party libraries
# ---------------------


from pydantic import BaseModel, BeforeValidator, AfterValidator, EmailStr, HttpUrl, ValidationError
from fastapi import HTTPException, status

from nixnox_dao import NICK_LEN, NAME_LEN
from .fastapi import app

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

# -----------------------------
# Pydantic validation functions
# -----------------------------


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


def v_nick(v: str) -> str:
    if len(v) > NICK_LEN:
        raise ValidationError(f"nickname too long: {len(v)} > {NICK_LEN}")
    return v


def v_fullname(v: str) -> str:
    if len(v) > NAME_LEN:
        raise ValidationError(f"full name too long: {len(v)} > {NAME_LEN}")
    return v


def v_password(v: str) -> str:
    if len(v) > PASSWD_LEN:
        raise ValidationError(f"password too long largo: {len(v)} > {PASSWD_LEN}")
    return v


def v_acronym(v: str) -> str:
    if len(v) > ACRONYM_LEN:
        raise ValidationError(f"acronym too long largo: {len(v)} > {ACRONYM_LEN}")
    return v


# --------------------
# Pydantic annotations
# --------------------

NickName = Annotated[str, AfterValidator(v_nick)]
FullName = Annotated[str, AfterValidator(v_fullname)]
Password = Annotated[str, AfterValidator(v_password)]
Acronym = Annotated[str, AfterValidator(v_acronym)]
DateTime = Annotated[Union[str, datetime, None], BeforeValidator(v_datetime)]


# ---------------
# Pydantic Models
# ---------------


class PersonCreate(BaseModel):
    nick: NickName
    password: Password
    fullname: FullName


class OrganizantionCreate(BaseModel):
    nick: NickName
    password: Password
    fullname: FullName
    acronym: Acronym
    website: HttpUrl
    email: EmailStr


@app.post(
    "/v1/persons",
    status_code=status.HTTP_201_CREATED,
    summary="Create person",
)
async def create_person(payload: PersonCreate):
    try:
        # llamada a tu DAO
        persona = dao_create_person(payload)
        return {
            "message": "person created",
            "person": persona.model_dump(exclude={"password"}),
        }
    except PersonAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "person_already_exists", "field": "nick"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_data", "reason": str(e)},
        )


@app.post(
    "/v1/organizations",
    status_code=status.HTTP_201_CREATED,
    summary="Create organization",
)
async def create_organization(payload: OrganizantionCreate):
    # aquí llamar a DAO para crear la persona
    try:
        # llamada a tu DAO
        persona = dao_create_organization(payload)
        return {
            "message": "organization created",
            "person": persona.model_dump(exclude={"password"}),
        }
    except OrgAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "aorganization already exists", "field": "nick"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_data", "reason": str(e)},
        )
