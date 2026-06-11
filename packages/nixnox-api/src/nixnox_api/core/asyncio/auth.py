# ----------------------------------------------------------------------
# Copyright (c) 2022
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# ----------------
# standard imports
# ----------------

import logging
import secrets
from datetime import datetime, timezone
from typing import Any, Tuple, Dict

# ---------------------
# Third party libraries
# ---------------------

from sqlalchemy import select

from nixnox_dao.auth.asyncio import User
from nixnox_dao.auth.utils import hash_password

# -----------
# own imports
# -----------

from ..model.auth import (
    verify_password,
    ApiKey,
    UserCreateInfo,
    UserModifyInfo,
    UserDeleteInfo,
    UserAuthenticateInfo,
    NickName,
)

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger(__name__.split(".")[-1])


# Session must point to the auth database
async def create_user(session: Any, info: UserCreateInfo) -> Dict[str, Any]:
    log.info("Creating user %s", info.login)
    user = (await session.scalars(select(User).where(User.login == info.login))).one_or_none()
    if user is not None:
        raise KeyError(f"User {user.login} already exists")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    user = User(
        login=info.login,
        password_hash=hash_password(info.password),
        full_name=info.full_name,
        role=info.role,
        api_key=secrets.token_urlsafe(32),
        created_at=now,
        updated_at=now,
    )
    session.add(user)
    return user.to_dict()


async def modify_user(session: Any, info: UserModifyInfo) -> Dict[str, Any]:
    log.info("Updating user %s", info.login)
    user = (await session.scalars(select(User).where(User.login == info.login))).one_or_none()
    if user is None:
        raise KeyError(f"User {info.login} does not exists")
    changed = False
    if info.full_name is not None:
        user.full_name = info.full_name
        changed = True
    if info.password is not None:
        user.password_hash = hash_password(info.password)
        changed = True
    if info.api_key:
        user.api_key = secrets.token_urlsafe(32)
        changed = True
    if info.role is not None and info.role != user.role:
        user.role = info.role
        changed = True
    if changed:
        user.updated_at = datetime.now(timezone.utc).replace(microsecond=0)
    return user.to_dict()


async def delete_user(session: Any, info: UserDeleteInfo) -> None:
    log.info("Deleting user %s", info.login)
    user = (await session.scalars(select(User).where(User.login == info.login))).one_or_none()
    if user is None:
        raise KeyError(f"User {info.login} does not exists")
    session.delete(user)


async def authenticate_user(session: Any, info: UserAuthenticateInfo) -> Tuple[bool, ApiKey | None]:
    """Autenticar usuario y devolver datos si es válido."""
    log.info("Authenticating user %s", info.login)
    user = (await session.scalars(select(User).where(User.login == info.login))).one_or_none()
    if user and verify_password(info.password, user["password_hash"]):
        return True, user.api_key
    return False, None


async def get_user_by_api_key(session: Any, api_key: ApiKey) -> Dict[str, Any] | None:
    user = (await session.scalars(select(User).where(User.api_key == api_key))).one_or_none()
    return user.to_dict() if user else None


async def get_user_by_login(session: Any, login: NickName) -> Dict[str, Any] | None:
    user = (await session.scalars(select(User).where(User.login == login))).one_or_none()
    return user.to_dict() if user else None
