# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import hashlib
import secrets

# ------------------
# Auxiliar functions
# ------------------


def hash_password(password: str) -> str:
    """Genera un hash de la contraseña"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return f"{salt}${password_hash}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica contraseña contra hash almacenado."""
    salt, stored_hash = password_hash.split("$")
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return new_hash == stored_hash
