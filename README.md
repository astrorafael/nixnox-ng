# nixnox-ng

Python develompent supporting the [NIXNOX project](https://guaix.fis.ucm.es/reecl/nixnox)
The development is divided in the following workspaces:
* `nixnox-dao`: The database model (vendor independent thanks to [SQLAlchemy](https://www.sqlalchemy.org/))
* `nixnox-core`. core components (functions, classes, etc.) for the Nixnox project
* `nixnox-tools`: CLI tools for the nixnox project.
* `nixnox-web`: Nixnox web interface, based on [Streamlit](https://streamlit.io/)

# Installation

1. Create a Python environment.
	```bash
	uv venv --python 3.12
	```
2. Install components
	```bash
	uv pip install nixnox-tools nixnox-web
	```
