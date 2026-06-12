import pytest


from nixnox_api.core.model import AuthRole, ObserverCreateReq, ObserverModifyReq


@pytest.fixture()
def admin_cre(request) -> ObserverCreateReq:
    return ObserverCreateReq(
        nickname="admin",
        password="1234",
        full_name="Admin User",
        role=AuthRole.ADMIN,
    )


@pytest.fixture()
def admin_mod(request) -> ObserverModifyReq:
    return ObserverModifyReq(
        nickname="admin",
        password="5678",
        new_api_key=True,
    )
