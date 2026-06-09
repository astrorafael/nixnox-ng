# ------------------
# Dynamic versioning
# ------------------

try:
    from importlib.metadata import version, PackageNotFoundError

    __version__ = version(__name__.split(".")[-1])
except (ImportError, PackageNotFoundError, LookupError):
    __version__ = "0.0.0+dev"

# ---------
# Reexports
# ---------

from nixnox_dao import hash_password


from .excp import AlreadyExistsError, InconsistentCoordinatesError


__all__ = [
    "__version__",
    "hash_password",
    "database_import",
    "database_export",
    "uploader",
    "AlreadyExistsError",
    "InconsistentCoordinatesError",
]
