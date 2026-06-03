try:
    from importlib.metadata import version, PackageNotFoundError

    __version__ = version(__name__.split(".")[-1])
except (ImportError, PackageNotFoundError, LookupError):
    __version__ = "0.0.0+dev"

from .constants import (
    ObserverType,
    ValidState,
    PhotometerModel,
    Temperature,
    Humidity,
    Coordinates,
    Timestamp,
    PopulationCentre,
)

from .utils import observer_name

__all__ = [
    "__version__",
    "observer_name",
    "ObserverType",
    "ValidState",
    "PhotometerModel",
    "Temperature",
    "Humidity",
    "Coordinates",
    "Timestamp",
    "PopulationCentre",
]
