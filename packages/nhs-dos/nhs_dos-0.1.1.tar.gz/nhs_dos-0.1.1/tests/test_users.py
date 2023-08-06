from nhs_dos import users


def test_user_constructor_returns_user_object():
    username = 'test-username'
    password = 'test-password'
    u = users.User(username, password)
    assert type(u) == users.User

