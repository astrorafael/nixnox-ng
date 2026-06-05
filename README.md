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

# Configuration

1. create a `.env` file to hold envirnoment variables
2. create a `.streamlit` directory and add two new files to it: `config.toml` `secrets.toml`

## Envirenmet variables

The following variables are needed:
```bash
NIXNOX_DB_URL=sqlite:///nixnox.db
# NIXNOX_DB_URL=sqlite+libsql://devel.db.sarna.dev:8080
AUTH_DB_URL==sqlite:///auth.db
```


