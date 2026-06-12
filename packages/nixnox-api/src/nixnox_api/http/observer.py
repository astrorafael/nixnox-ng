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


from pydantic import ValidationError
from fastapi import HTTPException, status, Header, Depends


# ----------
# own modules
# -----------

from .fastapi import app
from ..core.model import RoleType, PersonCreateReq, OrganizantionCreateReq


@app.post(
    "/v1/persons",
    status_code=status.HTTP_201_CREATED,
    summary="Create person",
)
async def create_person(payload: PersonCreateReq):
    try:
        # llamada a tu DAO
        payload.role = RoleType.USER # override any role passed
        persona = dao_create_person(payload)
        return {
            "message": "person created",
            "person": persona.model_dump(exclude={"password"}),
        }
    except PersonAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "person already exists", "field": "nickname"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid data", "reason": str(e)},
        )


@app.post(
    "/v1/organizations",
    status_code=status.HTTP_201_CREATED,
    summary="Create organization",
)
async def create_organization(payload: OrganizantionCreateReq):
    # aquí llamar a DAO para crear la persona
    try:
        # llamada a tu DAO
        payload.role = RoleType.USER # override any role passed
        persona = dao_create_organization(payload)
        return {
            "message": "organization created",
            "person": persona.model_dump(exclude={"password"}),
        }
    except OrgAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "organization already exists", "field": "nickname"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid data", "reason": str(e)},
        )


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "tu-clave":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )