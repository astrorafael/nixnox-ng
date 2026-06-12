import pytest


from nixnox_api.core.model import AuthRole, ObserverCreateReq, ObserverModifyReq


@pytest.fixture()
def admin_cre(request) -> ObserverCreateReq:
    return ObserverCreateReq(
        login="admin",
        password="1234",
        full_name="Admin User",
        role=AuthRole.ADMIN,
    )


@pytest.fixture()
def admin_mod(request) -> ObserverModifyReq:
    return ObserverModifyReq(
        login="admin",
        new_api_key=True,
    )
