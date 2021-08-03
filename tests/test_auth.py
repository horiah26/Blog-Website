"""Authentication and login/logout tests"""
from conftest import login, logout

def test_can_log_in(client):
    """Make sure login works."""

    rv = login(client, 'username1', 'password1')

    assert rv.status_code == 200

    assert b'You are logged in' in rv.data
    
def test_can_log_out(client):
    """Make sure logout works."""

    rv = login(client, 'username1', 'password1')

    assert rv.status_code == 200

    assert b'You are logged in' in rv.data

    rv = logout(client)
    
    assert b'You are logged out' in rv.data

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

def test_does_not_log_in_if_wrong_username(client):
    """Tests if page is not logged in if wrong password"""
    login = client.post('/login',
                data = dict(username='username312512',
                    password = 'password4'), follow_redirects=True)
    
    assert login.status_code == 200
    assert b'<input type="text" class="form-title" name="username"><br>' in login.data
    assert b'<input type="password" class="form-title" name="password"><br>' in login.data

    assert b'blog-description' not in login.data
    assert b'wrapper' not in login.data
    assert b'welcome' not in login.data

def test_does_not_log_in_if_empty_username(client):
    """Tests if page is not logged in if wrong password"""
    login = client.post('/login',
                data = dict(username='',
                    password = 'password4'), follow_redirects=True)
    
    assert b'Invalid username or password' in login.data

def test_does_not_log_in_if_empty_password(client):
    """Tests if page is not logged in if wrong password"""
    login = client.post('/login',
                data = dict(username='username312512',
                    password = ''), follow_redirects=True)
    
    assert b'Invalid username or password' in login.data

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

def test_cannot_sign_up_if_password_confirm_does_not_match(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username6',
                    name='Name nr 6',
                    email = 'username6@email.com',
                    password = 'password6',
                    confirm_password = 'password'), follow_redirects=True)

    assert b'Your password must match' in sign_up.data


    assert client.get('/').status_code == 200

def test_cannot_sign_up_if_user_exists(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username1',
                    name='Name nr 6',
                    email = 'username6@email.com',
                    password = 'password6',
                    confirm_password = 'password6'), follow_redirects=True)
    assert b'Username is already in use' in sign_up.data

    assert client.get('/').status_code == 200

def test_cannot_sign_up_if_email_already_used(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username6',
                    name='Name nr 6',
                    email = 'email1@g.com',
                    password = 'password6',
                    confirm_password = 'password6'), follow_redirects=True)
    assert b'Email adress is already in use' in sign_up.data

    assert client.get('/').status_code == 200

def test_cannot_sign_up_if_password_empty(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username6',
                    name='Name nr 6',
                    email = 'user1@email.com',
                    password = '',
                    confirm_password = 'password6'), follow_redirects=True)
    assert b'Password is required' in sign_up.data

    assert client.get('/').status_code == 200


def test_cannot_sign_up_if_username_empty(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='',
                    name='Name nr 6',
                    email = 'user1@email.com',
                    password = 'password6',
                    confirm_password = 'password6'), follow_redirects=True)
    assert b'Username is required' in sign_up.data

    assert client.get('/').status_code == 200
    

def test_cannot_sign_up_if_name_empty(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username 6',
                    name='',
                    email = 'user1@email.com',
                    password = 'password6',
                    confirm_password = 'password6'), follow_redirects=True)
    assert b'Your name is required' in sign_up.data

    assert client.get('/').status_code == 200
    

def test_cannot_sign_up_if_email_empty(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username 6',
                    name='Name nr 6',
                    email = '',
                    password = 'password6',
                    confirm_password = 'password6'), follow_redirects=True)
    assert b'Email is required' in sign_up.data

    assert client.get('/').status_code == 200


def test_cannot_sign_up_if_confirm_password_empty(client):
    """Tests if user can sign up"""
    sign_up = client.post('/signup',
                data = dict(username='username 6',
                    name='Name nr 6',
                    email = 'user1@email.com',
                    password = 'password6',
                    confirm_password = ''), follow_redirects=True)
    assert b'Please confirm your password' in sign_up.data

    assert client.get('/').status_code == 200


def test_can_log_in_user_redirects_to_homepage(client):
    """Tests if page is rediected after log in"""
    login = client.post('/login',
                data = dict(username='username3',
                    password = 'password3'), follow_redirects=True)

    assert login.status_code == 200

    assert b'blog-description' in login.data
    assert b'wrapper' in login.data
    assert b'welcome' in login.data