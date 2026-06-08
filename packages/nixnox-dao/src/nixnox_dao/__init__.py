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
    NICK_LEN,
    EMAIL_LEN,
    PLACE_LEN,
    POPUCEN_LEN,
    SUBREG_LEN,
    REGION_LEN,
    COUNTRY_LEN,
    TZONE_LEN,
    PHOT_NAME,
    COMMENT_LEN,
    IDENT_LEN,
    DIGEST_LEN,
    WEATHER_LEN,
    URL_LEN,
    OTHEROBS_LEN
)
from .auth.constants import AuthRole, LOGIN_LEN, HASH_LEN, NAME_LEN, APIKEY_LEN

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
    "LOGIN_LEN",
    "HASH_LEN",
    "NAME_LEN",
    "APIKEY_LEN",
    "NICK_LEN",
    "EMAIL_LEN",
    "PLACE_LEN",
    "POPUCEN_LEN",
    "SUBREG_LEN",
    "REGION_LEN",
    "COUNTRY_LEN",
    "TZONE_LEN",
    "PHOT_NAME",
    "COMMENT_LEN",
    "IDENT_LEN",
    "DIGEST_LEN",
    "WEATHER_LEN",
    "URL_LEN",
    "OTHEROBS_LEN",
]
