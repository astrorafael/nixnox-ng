# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

from typing import Type

# ---------------------
# Third party libraries
# ---------------------

from lica.sqlalchemy.noasync.model import Model

# -------------------
# Own package imports
# -------------------

from nixnox_dao.nixnox.model import (
    make_Time,
    make_Date,
    make_Observer,
    make_Person,
    make_Organization,
    make_Location,
    make_Photometer,
    make_Observation,
    make_Measurement,
)


# Tables creation with the no async Model behaviour built-in

# NIXNOX Data Access Objects
Date: Type = make_Date(Model)
Time: Type = make_Time(Model)
Observer: Type = make_Observer(Model)
Person: Type = make_Person(Observer)
Organization = make_Organization(Observer)
Location: Type = make_Location(Model)
Photometer: Type = make_Photometer(Model)
Observation: Type = make_Observation(Model)
Measurement: Type = make_Measurement(Model)



__all__ = [
    "Date",
    "Time",
    "Observer",
    "Location",
    "Photometer",
    "Observation",
    "Measurement",
]
