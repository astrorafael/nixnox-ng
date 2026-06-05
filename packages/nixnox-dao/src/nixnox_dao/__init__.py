# ------------------
# Dynamic versioning
# ------------------

try:
    from importlib.metadata import version, PackageNotFoundError

    __version__ = version(__name__.split(".")[-1])
except (ImportError, PackageNotFoundError, LookupError):
    __version__ = "0.0.0+dev"

# ---------
# Reimports
# ---------

from .nixnox.constants import (
    ObserverType,
    ValidState,
    PhotometerModel,
    Temperature,
    Humidity,
    Coordinates,
    Timestamp,
    PopulationCentre,
)

from .auth.constants import AuthRole

__all__ = [
    "__version__",
    "ObserverType",
    "ValidState",
    "PhotometerModel",
    "Temperature",
    "Humidity",
    "Coordinates",
    "Timestamp",
    "PopulationCentre",
    "AuthRole",
]
