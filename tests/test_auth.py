"""Authentication and login/logout tests"""
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

    assert b'You have signed up' in sign_up.data


    assert client.get('/').status_code == 200

def test_can_log_in(client):
    """Make sure login and logout works."""

    rv = login(client, 'username1', 'password1')

    assert rv.status_code == 200

    assert b'You are logged in' in rv.data

    logout(client)
