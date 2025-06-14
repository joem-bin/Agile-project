def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data  # Optional: make sure login form is shown
