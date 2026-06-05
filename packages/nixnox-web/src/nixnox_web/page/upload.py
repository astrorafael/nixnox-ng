# ---------------
# Standard library
# ---------------

import time
from pathlib import Path

# ---------
# STREAMLIT
# ---------

import streamlit as st
import streamlit.logger
from streamlit.connections import SQLConnection

# ---------------
# Other libraries
# ---------------

import nixnox_core as nx

# ----------------
# Global variables
# ----------------

log = streamlit.logger.get_logger(__name__)
log.info("ENTERING UPLOAD PAGE")

# Database connection
conn = st.connection("env:NX_ENV", type="sql")


def view_upload(conn: SQLConnection):
    st.title("Upload TAS files to database")
    data = st.file_uploader("*ECSV File only!*", type=["ecsv"])
    if data:
        with conn.session as session:
            try:
                observation = nx.uploader(session, data, log=log)
            except nx.AlreadyExistsError as e:
                observation = e.args[0]
                st.error("Error: observation already exists in the database", icon="🚨")
            except Exception as e:
                st.write(e)
                st.error("Error: Invalid file format", icon="🚨")
            else:
                st.info(f"Observation upload to database: {observation.identifier}", icon="ℹ️")
                time.sleep(2)
                del st.session_state.result_table
                st.switch_page(Path(__file__).parent / "home.py")


view_upload(conn)
