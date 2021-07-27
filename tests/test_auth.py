"""Authentication and login/logout tests"""
import pytest
from conftest import login, logout

def test_does_not_log_in_if_wrong_password(client):
    """Tests if page is not logged in if wrong password"""
    login = client.post('/login',
                data = dict(username='username3',
                    password = 'password4'), follow_redirects=True)

    assert login.status_code == 200

    assert b'<input type="text" class="form-title" name="username"><br>' in login.data
    assert b'<input type="password" class="form-title" name="password"><br>' in login.data

    assert b'blog-description' not in login.data
    assert b'wrapper' not in login.data
    assert b'welcome' not in login.data


def test_can_sign_up_user(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username5',
                    name='Name nr 5',
                    email = 'username5@email.com',
                    password = 'password5',
                    confirm_password = 'password5'), follow_redirects=True)

    assert sign_up.status_code == 200


    assert client.get('/').status_code == 200

def test_can_log_in(client):
    """Make sure login and logout works."""

    rv = login(client, 'username1', 'password1')

    assert rv.status_code == 200

    assert b'You are logged in' in rv.data

    logout(client)

def test_does_not_write_article_if_not_logged_in(client):
    """Cannot write article if not logged_in"""
    redirect = client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'), follow_redirects=True)

    assert b'You must be logged in to do this' in redirect.data

def test_cannot_delete_post_if_not_logged_in(client):
    """Can delete post"""
    logout(client)
    assert client.get('/3/').status_code == 200

    rv = client.get('/3/delete', follow_redirects=True)
    assert b'You don&#39;t have permission to modify this post' in rv.data
    assert client.get('/3/').status_code == 200

def test_cannot_delete_post_if_logged_in_as_another_user(client):
    """Cannot delete post if logged in as another user"""
    rv = login(client, 'username2', 'password2')
    assert client.get('/3/').status_code == 200

    rv = client.get('/3/delete', follow_redirects=True)
    assert b'You don&#39;t have permission to modify this post' in rv.data
    assert client.get('/3/').status_code == 200

    logout(client)

def test_can_delete_post_if_logged_in(client):
    """Can delete post"""
    login(client, 'username1', 'password1')
    assert client.get('/3/').status_code == 200

    client.get('/3/delete')

    assert b'Post not found' in client.get('/3/', follow_redirects=True).data
    logout(client)


def test_admin_can_edit_another_user_profile(client):
    """Does not update an article if the input is an empty title"""
    logout(client)
    login(client, 'admin','admin')
    before = client.get('/users/username1/')
    assert  b"username1" in before.data

    client.post('/users/username1/edit',
            data = dict(name='new name for test1',
                        email='Ugly text for test sdhsdjherj3eh12k;op1',
                        password='',
                        confirm_password=''), follow_redirects = True)

    after = client.get('/users/username1/')
    print (after.data)
    assert b'new name for test' in after.data
    assert b'Ugly text for test sdhsdjherj3eh12k;op' in after.data

def test_admin_can_delete_another_user_profile(client):
    """Does not update an article if the input is an empty title"""
    logout(client)
    login(client, 'admin','admin')
    before = client.get('/users/username2/')
    assert b"username2" in before.data
    assert b'username2' in client.get('/users').data

    rv = client.get('/users/username2/delete', follow_redirects = True)
    assert rv.status_code == 200
    assert b'User deleted' in rv.data
    assert not b'username2' in client.get('/users').data
    logout(client)

def test_user_cannot_edit_another_user_profile(client):
    """Does not update an article if the input is an empty title"""
    logout(client)
    login(client, 'username3','password3')
    before = client.get('/users/username1/')
    assert  b"username1" in before.data

    rv = client.post('/users/username1/edit',
            data = dict(name='new name for test',
                        text='Ugly text for test sdhsdjherj3eh12k;op'), follow_redirects = True)

    assert b'You don&#39;t have permission to modify this profile' in rv.data
    logout(client)

def test_user_cannot_delete_another_user_profile(client):
    """Does not update an article if the input is an empty title"""
    logout(client)
    login(client, 'username3','password3')
    before = client.get('/users/username1/')
    assert  b"username1" in before.data

    rv = client.get('/users/username1/delete', follow_redirects = True)

    assert b'You don&#39;t have permission to modify this profile' in rv.data
    logout(client)
