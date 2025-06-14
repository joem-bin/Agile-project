# tests/conftest.py

import pytest
from app import app  # Your Flask app from app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enables exceptions to bubble up
    app.config['WTF_CSRF_ENABLED'] = False  # Optional, if you're using forms
    with app.test_client() as client:
        yield client


