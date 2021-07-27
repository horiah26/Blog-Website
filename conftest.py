"""Fixtures and methods common among multiple test files"""
import pytest
from app import create_app

@pytest.fixture()
def client():
    """Creates the client fixture"""
    app = create_app()
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = "memory")
    app.app_context().push()
    yield app.test_client()

def login(client, username, password):
    """Logs user in"""
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Logs user out"""
    return client.get('/logout', follow_redirects=True)
