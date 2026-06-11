from lica.sqlalchemy.asyncio.dbase import create_engine_sessionclass

engine, Session = create_engine_sessionclass(env_var="AUTH_DB_URL", tag="authdb")

__all__ = ["engine", "Session"]
