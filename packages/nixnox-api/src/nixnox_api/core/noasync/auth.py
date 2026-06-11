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
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Any, Tuple

# ---------------------
# Third party libraries
# ---------------------

from sqlalchemy import select

from nixnox_dao.auth.noasync import User
from nixnox_dao.auth.utils import hash_password

# -----------
# own imports
# -----------

from ..model.auth import (
    ApiKey,
    UserCreateInfo,
    UserModifyInfo,
    UserDeleteInfo,
    UserAuthenticateInfo,
    UserLookupByApiKey,
)

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger(__name__.split(".")[-1])

# ------------------
# Auxiliar functions
# ------------------


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica contraseña contra hash almacenado."""
    salt, stored_hash = password_hash.split("$")
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return new_hash == stored_hash


# Session must point to the auth database
def create_user(session: Any, info: UserCreateInfo) -> None:
    with session.begin():
        user = session.scalars(select(User).where(User.login == info.login)).one_or_none()
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
    with session.begin():
        session.add(user)


def modify_user(session: Any, info: UserModifyInfo) -> None:
    log.info("Updating user %s", info.login)
    with session.begin():
        user = session.scalars(select(User).where(User.login == info.login)).one_or_none()
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


def delete_user(session: Any, info: UserDeleteInfo) -> None:
    log.info("Deleting user %s", info.login)
    with session.begin():
        user = session.scalars(select(User).where(User.login == info.login)).one_or_none()
        if user is None:
            raise KeyError(f"User {info.login} does not exists")
        session.delete(user)


def authenticate_user(session: Any, info: UserAuthenticateInfo) -> Tuple[bool, ApiKey | None]:
    """Autenticar usuario y devolver datos si es válido."""
    log.info("Authenticating user %s", info.login)
    with session.begin():
        user = session.scalars(select(User).where(User.login == info.login)).one_or_none()
        if user and verify_password(info.password, user["password_hash"]):
            return True, user.api_key
        return False, None


def get_user_by_api_key(session: Any, info: UserLookupByApiKey) -> dict | None:
    with session.begin():
        user = session.scalars(select(User).where(User.api_key == info.api_key)).one_or_none()
        return user.to_dict() if user else None
