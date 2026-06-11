import pytest


from nixnox_api.core.model.auth import UserCreateInfo, AuthRole


@pytest.fixture()
def admin(request) -> UserCreateInfo:
    return UserCreateInfo(
        login="admin",
        password="1234",
        full_name="Admin User",
        role=AuthRole.ADMIN,
    )
