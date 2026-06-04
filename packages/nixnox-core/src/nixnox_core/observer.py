# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

from nixnox_dao import ObserverType


def observer_name(observer: dict) -> str:
    """Handy formatting tool to get a good observer name"""

    if ObserverType(observer["type"]) == ObserverType.PERSON:
        name = observer["name"]
        if observer["affiliation"] is not None:
            long_affil = observer["affiliation"]["org_name"]
            short_affil = (
                observer["affiliation"]["org_acronym"]
                if observer["affiliation"]["org_acronym"] is not None
                else ""
            )
            affiliation = short_affil or long_affil
            result = f"{name} ({affiliation})"
        else:
            result = name
    else:
        name = observer["org_name"]
        result = f"{name} ({observer['org_acronym']})" if observer["org_acronym"] else name
    return result
