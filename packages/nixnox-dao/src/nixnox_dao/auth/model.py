# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------


# --------------------
# System wide imports
# -------------------


from typing import Type
from datetime import datetime

# ---------------------
# Third party libraries
# ---------------------


from sqlalchemy import (
    Enum,
    String,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column

from lica.sqlalchemy.metadata import metadata

# -----------
# Own modules
# -----------

from .constants import AuthRole

# ================
# Module constants
# ================


# ---------------------------------------------
# Additional conveniente types for enumerations
# ---------------------------------------------

# These are really Column declarations
# They are needed on the RHS of the ORM model, in mapped_column()


RoleCol: Enum = Enum(
    AuthRole,
    name="role_type",
    create_constraint=False,
    metadata=metadata,
    validate_strings=True,
    values_callable=lambda x: [e.name for e in x],
)


# --------
# Entities
# --------


def make_User(declarative_base: Type) -> Type:
    class User(declarative_base):
        __tablename__ = "user_t"

        # User Id
        user_id: Mapped[int] = mapped_column(primary_key=True)
        # login string
        username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
        # password stoired in hashed form
        password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
        # authentication role
        role: Mapped[AuthRole] = mapped_column(RoleCol, nullable=False)
        # User full name
        full_name: Mapped[str] = mapped_column(String(128), nullable=False)
        # URL-safe, 32 bytes base64 encoded API Key
        api_key: Mapped[str] = mapped_column(String(64), unique=True)
        # Creation date
        created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
        # Last update
        updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

        def __repr__(self) -> str:
            return (
                "User("
                f"user_id={self.user_id!r}, "
                f"username={self.username!r}, "
                f"role={self.role!r}, "
                f"api_key={self.api_key!r}, "
                f"full_name={self.full_name!r}, "
                f"password_hash={self.password_hash!r}, "
                f"created_at={self.created_at!r}, "
                f"updated_at={self.updated_at!r}"
                ")"
            )

    return User
