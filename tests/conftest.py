import os
import pytest
import sqlite3
from dotenv import load_dotenv
load_dotenv()

from database_operations import get_db_connection
import app as flask_app_module

@pytest.fixture
def client():
    flask_app_module.app.config['TESTING'] = True
    with flask_app_module.app.test_client() as client:
        yield client




@pytest.fixture(scope='function', autouse=True)
def temp_db(monkeypatch):
    test_db = "temp_test.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    monkeypatch.setattr("database_operations.DB_NAME", test_db)

    conn = sqlite3.connect(test_db)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    yield

    if os.path.exists(test_db):
        os.remove(test_db)
