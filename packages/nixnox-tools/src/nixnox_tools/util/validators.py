# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import os
import functools


# ---------------------------
# Third-party library imports
# ----------------------------

from lica.validators import vfile

# -------------------
# Auxiliary functions
# -------------------

def _vextension(path: str, extension: str) -> str:
    _, ext = os.path.splitext(path)
    if ext != extension:
        # Can't use ValueError inside a functools.partial function
        raise Exception(f"Path does not end with {extension} extension")
    return path

# --------------------
# Exportable functions
# --------------------

vecsv = functools.partial(_vextension, extension=".ecsv")
vtxt = functools.partial(_vextension, extension=".txt")

def vecsvfile(path: str) -> str:
    path = vfile(path)
    return vecsv(path)

def vtxtfile(path: str) -> str:
    path = vfile(path)
    return vtxt(path)
