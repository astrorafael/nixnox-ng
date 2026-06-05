# ---------------
# Standard library
# ---------------

from pathlib import Path

# ---------
# STREAMLIT
# ---------

import streamlit as st

# ==========================
# WEB APPPLICATION STRUCTURE
# ==========================
st.set_page_config(page_title="NIXNOX", layout="wide", page_icon=":material/moon_stars:")
pg = st.navigation(
    [
        st.Page(
            Path(__file__).parent / "page" / "home.py",
            title="Observations List",
            icon=":material/list:",
        ),
        st.Page(
            Path(__file__).parent / "page" / "observation.py",
            title="Observation details",
            icon=":material/zoom_in:",
        ),
        st.Page(
            Path(__file__).parent / "page" / "plot.py",
            title="Observation plot",
            icon=":material/graph_7:",
        ),
        st.Page(
            Path(__file__).parent / "page" / "upload.py",
            title="Upload observation file",
            icon=":material/upload_file:",
        ),
        st.Page(
            Path(__file__).parent / "page" / "observer.py",
            title="Edit observer",
            icon=":material/edit:",
        ),
    ]
)
pg.run()
