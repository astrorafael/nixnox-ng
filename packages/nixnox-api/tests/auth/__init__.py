from lica.sqlalchemy.noasync.dbase import create_engine_sessionclass

engine, Session = create_engine_sessionclass(env_var="AUTH_DB_URL", tag="nixnoxdb")

__all__ = ["engine", "Session"]
