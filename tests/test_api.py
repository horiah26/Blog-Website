"""API test"""
from conftest import login, logout


def test_can_change_post_image(client):
    """Sends the correct post number to the js function"""

    rv = client.get('/4/')
    print(rv.data)
    assert b'onload="onLoad(4)"' in rv.data
