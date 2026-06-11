import pytest


from nixnox_api.core.model.auth import AuthRole, UserCreateInfo, UserModifyInfo


@pytest.fixture()
def admin(request) -> UserCreateInfo:
    return UserCreateInfo(
        login="admin",
        password="1234",
        full_name="Admin User",
        role=AuthRole.ADMIN,
    )


@pytest.fixture()
def admin1(request) -> UserModifyInfo:
    return UserModifyInfo(
        login="admin",
        full_name="The Admin User",
        api_key=True,
    )
