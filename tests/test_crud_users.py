from database_operations import insert_user, get_user


def test_insert_and_login_user():
    success = insert_user("joe", "joe@example.com", "securepass", "user")
    assert success

    user = get_user("joe", "securepass")
    assert user is not None
    assert isinstance(user[0], int)
    assert user[1] == "user"


def test_login_with_wrong_password():
    insert_user("alice", "alice@mail.com", "correct", "admin")
    user = get_user("alice", "wrongpass")
    assert user is None
