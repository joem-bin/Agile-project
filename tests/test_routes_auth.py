def test_home_route_shows_login_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b'<h2 class="govuk-heading-m">Login' in res.data
    assert b"Create New Account" in res.data


def test_login_with_missing_fields(client):
    res = client.post(
        "/login", data={"username": "", "password": ""}, follow_redirects=True
    )
    assert b"Username and password are required" in res.data
    assert res.status_code == 200


def test_login_with_invalid_credentials(client):
    res = client.post(
        "/login",
        data={"username": "notarealuser", "password": "wrongpass"},
        follow_redirects=True,
    )
    assert b"Incorrect username or password" in res.data
    assert res.status_code == 200


def test_signup_with_mismatched_passwords(client):
    res = client.post(
        "/signup",
        data={
            "username": "tester",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password124",
            "role": "user",
        },
        follow_redirects=True,
    )
    assert b"Passwords do not match" in res.data
    assert res.status_code == 200


def test_signup_with_weak_password(client):
    res = client.post(
        "/signup",
        data={
            "username": "weakpass",
            "email": "weak@example.com",
            "password": "123",
            "confirm_password": "123",
            "role": "user",
        },
        follow_redirects=True,
    )
    assert b"Password must be at least 6 characters" in res.data
    assert res.status_code == 200
