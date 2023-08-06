import pytest
from nhs_dos import RestApiClient, User


def test_new_restclient_without_user_throws_exception():
    with pytest.raises(TypeError):
        RestApiClient()


def test_new_restclient_with_user_returns_properly():
    u = User('username', 'password')
    r = RestApiClient(u)
    assert type(r) is RestApiClient
