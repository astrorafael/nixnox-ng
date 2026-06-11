import pytest
import logging
from argparse import Namespace

from lica.sqlalchemy import sqa_logging

from nixnox_api.core.model.auth import APIKEY_LEN
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


def test_create_user(session, admin):
    with session.begin():
        user = create_user(session=session, info=admin)
        assert user["login"] == admin.login
        assert user["role"] == admin.role
        assert user["full_name"] == admin.full_name
        assert len(user["api_key"]) == APIKEY_LEN


def test_modif_user(session, admin1):
    with session.begin():
        user = get_user_by_login(session=session, login=admin1.login)
        assert user is not None
        old_api_key = user["api_key"]
        user = modify_user(session=session, info=admin1)
        assert user["login"] == admin1.login
        assert user["role"] == admin1.role
        assert user["full_name"] == admin1.full_name
        assert user["api_key"] != old_api_key
