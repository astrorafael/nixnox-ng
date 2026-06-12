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
from nixnox_dao import TOKEN_LEN, hash_password, verify_password
from nixnox_dao.auth.noasync import User

# -----------
# own imports
# -----------

from ..model import (
    ApiKey,
    AuthRole,
    NickName,
    Password,
)

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger(__name__.split(".")[-1])


# Session must point to the auth database
async def create_user(
    session: Any, login: NickName, password: Password, role: AuthRole
) -> Dict[str, Any]:
    log.info("Creating user %s", login)
    user = (await session.scalars(select(User).where(User.login == login))).one_or_none()
    if user is not None:
        raise KeyError(f"User {user.login} already exists")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    user = User(
        login=login,
        password_hash=hash_password(password),
        role=role,
        api_key=secrets.token_urlsafe(32),
        created_at=now,
        updated_at=now,
    )
    session.add(user)
    return user.to_dict()


async def modify_user(
    session: Any,
    login: NickName,
    password: Password = None,
    role: AuthRole = None,
    new_api_key: bool = False,
) -> None:
    log.info("Updating user %s", login)
    user = (await session.scalars(select(User).where(User.login == login))).one_or_none()
    if user is None:
        raise KeyError(f"User {login} does not exists")
    changed = False
    if password is not None:
        user.password_hash = hash_password(password)
        changed = True
    if new_api_key:
        user.api_key = secrets.token_urlsafe(32)
        changed = True
    if role is not None and role != user.role:
        user.role = role
        changed = True
    if changed:
        user.updated_at = datetime.now(timezone.utc).replace(microsecond=0)
    


async def delete_user(session: Any, login: NickName) -> None:
    log.info("Deleting user %s", login)
    user = (await session.scalars(select(User).where(User.login == login))).one_or_none()
    if user is None:
        raise KeyError(f"User {login} does not exists")
    session.delete(user)


async def authenticate_user(
    session: Any, login: NickName, password: Password
) -> Tuple[bool, ApiKey | None]:
    """Autenticar usuario y devolver datos si es válido."""
    log.info("Authenticating user %s", login)
    user = (await session.scalars(select(User).where(User.login == login))).one_or_none()
    if user and verify_password(password, user.password_hash):
        return True, user.api_key
    return False, None


async def get_user_by_api_key(session: Any, api_key: ApiKey) -> Dict[str, Any] | None:
    user = (await session.scalars(select(User).where(User.api_key == api_key))).one_or_none()
    return user.to_dict() if user else None


async def get_user_by_login(session: Any, login: NickName) -> Dict[str, Any] | None:
    user = (await session.scalars(select(User).where(User.login == login))).one_or_none()
    return user.to_dict() if user else None
