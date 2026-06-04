# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import os

# ---------------------
# Third party libraries
# ---------------------

import streamlit as st


# ---------
# Functions
# ---------

def ttl() -> str:
	"""get the Cache Time to live as a function of the development environment"""
	env = os.environ.get("NX_ENV", "prod")
	return st.secrets["cache"][env]["ttl"]
