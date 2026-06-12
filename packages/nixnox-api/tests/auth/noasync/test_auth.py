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
def admin1(session, admin_cre) -> dict[str, Any]:
    with session.begin():
        user = create_user(
            session=session, login=admin_cre.nickname, password=admin_cre.password, role=admin_cre.role
        )
        return user

@pytest.fixture(scope="function")
def admin2(session, admin_cre, admin_mod) -> dict[str, Any]:
    with session.begin():
        create_user(
            session=session, login=admin_cre.nickname, password=admin_cre.password, role=admin_cre.role
        )
    with session.begin():
        modify_user(session=session, login=admin_mod.nickname, password=admin_mod.password, new_api_key=admin_mod.new_api_key)
    with session.begin():    
        user = get_user_by_login(session=session, login=admin_mod.nickname)
        return user
        


def test_create_user(session, admin_cre):
    with session.begin():
        user = create_user(
            session=session, login=admin_cre.nickname, password=admin_cre.password, role=admin_cre.role
        )
        assert user["login"] == admin_cre.nickname
        assert user["role"] == admin_cre.role
        assert len(user["api_key"]) == APIKEY_LEN


def test_read_user(session, admin1):
    with session.begin():
        user = get_user_by_login(session=session, login=admin1["login"])
        assert user is not None


def test_modif_user(session, admin_mod, admin1):
    with session.begin():
        user = get_user_by_login(session=session, login=admin_mod.nickname)
        assert user is not None
        old_api_key = user["api_key"]
        modify_user(session=session, login=admin_mod.nickname, new_api_key=admin_mod.new_api_key)
    with session.begin():
        user = get_user_by_login(session=session, login=admin_mod.nickname)
        assert user["login"] == admin_mod.nickname
        assert user["api_key"] != old_api_key

def test_authenticate_user_1(session, admin1, admin_cre):
    with session.begin():
        user = get_user_by_login(session=session, login=admin_cre.nickname)
        result, api_key = authenticate_user(session=session, login=admin_cre.nickname, password=admin_cre.password)
        assert result == True

def test_authenticate_user_2(session, admin2, admin_cre):
    with session.begin():
        user = get_user_by_login(session=session, login=admin_cre.nickname)
        result, api_key = authenticate_user(session=session, login=admin_cre.nickname, password=admin_cre.password)
        assert result == False

def test_api_key(session, admin1):
    with session.begin():
        user = get_user_by_api_key(session=session, api_key="foo")
        assert user is None
        user = get_user_by_api_key(session=session, api_key=admin1["api_key"])
        assert user is not None and user["api_key"] == admin1["api_key"]

