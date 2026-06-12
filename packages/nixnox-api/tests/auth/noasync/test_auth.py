import pytest
import logging
from argparse import Namespace
from typing import Any

from lica.sqlalchemy import sqa_logging

from nixnox_api.core.model import APIKEY_LEN
from nixnox_api.core.noasync.auth import (
    create_user,
    modify_user,
    delete_user,
    authenticate_user,
    get_user_by_api_key,
    get_user_by_login,
)

from . import engine, Session
from ... import DbSize, copy_file

log = logging.getLogger(__name__.split(".")[-1])


@pytest.fixture(scope="function", params=[DbSize.SMALL])
def session(request):
    args = Namespace(verbose=True)
    sqa_logging(args)
    copy_file(f"auth.{request.param}.db", "auth.db")
    yield Session()
    log.info("Teardown code empty so far")
    engine.dispose()


@pytest.fixture(scope="function")
def admin(session, admin_cre) -> dict[str, Any]:
    with session.begin():
        user = create_user(
            session=session, login=admin_cre.login, password=admin_cre.password, role=admin_cre.role
        )
        return user


def test_create_user(session, admin_cre):
    with session.begin():
        user = create_user(
            session=session, login=admin_cre.login, password=admin_cre.password, role=admin_cre.role
        )
        assert user["login"] == admin_cre.login
        assert user["role"] == admin_cre.role
        assert len(user["api_key"]) == APIKEY_LEN


def test_read_user(session, admin):
    with session.begin():
        user = get_user_by_login(session=session, login=admin["login"])
        assert user is not None


def test_modif_user(session, admin_mod, admin):
    with session.begin():
        user = get_user_by_login(session=session, login=admin_mod.login)
        assert user is not None
        old_api_key = user["api_key"]
        user = modify_user(session=session, login=admin_mod.login, new_api_key=admin_mod.new_api_key)
        assert user["login"] == admin_mod.login
        assert user["api_key"] != old_api_key
