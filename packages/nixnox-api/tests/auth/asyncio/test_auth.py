import pytest
import pytest_asyncio

import logging
from argparse import Namespace
from typing import Any

from lica.sqlalchemy import sqa_logging

from nixnox_api.core.model import APIKEY_LEN
from nixnox_api.core.asyncio.auth import (
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


@pytest_asyncio.fixture(scope="function", params=[DbSize.SMALL])
async def session(request):
    args = Namespace(verbose=True)
    sqa_logging(args)
    copy_file(f"auth.{request.param}.db", "auth.db")
    yield Session()
    log.info("Teardown code disposes the engine")
    await engine.dispose()



@pytest_asyncio.fixture(scope="function")
async def admin1(session, admin_cre) -> dict[str, Any]:
    async with session.begin():
        user = await create_user(
            session=session, login=admin_cre.login, password=admin_cre.password, role=admin_cre.role
        )
        return user

@pytest_asyncio.fixture(scope="function")
async def admin2(session, admin_cre, admin_mod) -> dict[str, Any]:
    async with session.begin():
        await create_user(
            session=session, login=admin_cre.login, password=admin_cre.password, role=admin_cre.role
        )
    async with session.begin():
        await modify_user(session=session, login=admin_mod.login, password=admin_mod.password, new_api_key=admin_mod.new_api_key)
    async with session.begin():    
        user = await get_user_by_login(session=session, login=admin_mod.login)
        return user


@pytest.mark.asyncio
async def test_create_user(session, admin_cre):
    async with session.begin():
        user = await create_user(
            session=session, login=admin_cre.login, password=admin_cre.password, role=admin_cre.role
        )
        assert user["login"] == admin_cre.login
        assert user["role"] == admin_cre.role
        assert len(user["api_key"]) == APIKEY_LEN

@pytest.mark.asyncio
async def test_read_user(session, admin1):
    async with session.begin():
        user = await get_user_by_login(session=session, login=admin1["login"])
        assert user is not None

@pytest.mark.asyncio
async def test_modif_user(session, admin_mod, admin1):
    async with session.begin():
        user = await get_user_by_login(session=session, login=admin_mod.login)
        assert user is not None
        old_api_key = user["api_key"]
        await modify_user(session=session, login=admin_mod.login, new_api_key=admin_mod.new_api_key)
    async with session.begin():
        user = await get_user_by_login(session=session, login=admin_mod.login)
        assert user["login"] == admin_mod.login
        assert user["api_key"] != old_api_key

@pytest.mark.asyncio
async def test_authenticate_user_1(session, admin1, admin_cre):
    async with session.begin():
        user = await get_user_by_login(session=session, login=admin_cre.login)
        result, api_key = await authenticate_user(session=session, login=admin_cre.login, password=admin_cre.password)
        assert result == True

@pytest.mark.asyncio
async def test_authenticate_user_2(session, admin2, admin_cre):
    async with session.begin():
        user = await get_user_by_login(session=session, login=admin_cre.login)
        result, api_key = await authenticate_user(session=session, login=admin_cre.login, password=admin_cre.password)
        assert result == False

@pytest.mark.asyncio
async def test_api_key(session, admin1):
    async with session.begin():
        user = await get_user_by_api_key(session=session, api_key="foo")
        assert user is None
        user = await get_user_by_api_key(session=session, api_key=admin1["api_key"])
        assert user is not None and user["api_key"] == admin1["api_key"]

