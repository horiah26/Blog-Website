"""User tests"""
import datetime
from conftest import login, logout

def test_shows_posts_on_user_profile(client):
    """Shows posts on user profile"""
    rv = client.get('/users/username1/')
    assert b'Duis a lectus in erat blandit hendrerit' in rv.data
    assert b'Quisque tempor fringilla velit et accumsan. Cras vitae purus sit amet tellus tempor facilisis' in rv.data

def test_shows_info_on_user_profile(client):
    """Shows info on user profile"""
    rv = client.get('/users/username1/')
    assert b'Name 1\'s Profile' in rv.data
    assert b'Email: email1@g.com' in rv.data
    assert b'Username: username1' in rv.data
    time_now = datetime.datetime.now().strftime("%B %d %Y")

    assert bytes(f"Date joined: {time_now}", 'utf-8') in rv.data
    assert bytes(f"Profile last modified: {time_now}", 'utf-8') in rv.data

def test_user_can_edit_own_profile(client):
    """Does not update an article if the input is an empty title"""
    logout(client)
    login(client, 'username4','password4')
    before = client.get('/users/username4/')
    assert  b"username4" in before.data

    client.post('/users/username4/edit',
            data = dict(name='new name for test4',
                        email='Ugly text for test sdhsdjherj3eh12k;op4',
                        password='',
                        confirm_password=''), follow_redirects = True)

    after = client.get('/users/username4/')
    assert b'new name for test4' in after.data
    assert b'Ugly text for test sdhsdjherj3eh12k;op4' in after.data

def test_user_can_delete_own_profile(client):
    """Does user can delete own profile"""
    logout(client)
    login(client, 'username4','password4')
    before = client.get('/users/username4/')
    assert b"username4" in before.data

    rv = client.get('/users/username4/delete', follow_redirects = True)
    assert rv.status_code == 200
    assert b'User deleted' in rv.data
    assert not b'username4' in client.get('/users').data
    logout(client)

def test_admin_can_edit_another_user_profile(client):
    """Admin can edit another user's profile"""
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
    """Admin can delete another user's profile"""
    logout(client)
    login(client, 'admin','admin')
    before = client.get('/users/username3/')
    assert b"username3" in before.data
    assert b'username3' in client.get('/users').data

    rv = client.get('/users/username3/delete', follow_redirects = True)
    assert rv.status_code == 200
    assert b'User deleted' in rv.data
    assert not b'username3' in client.get('/users').data
    logout(client)

def test_user_cannot_edit_another_user_profile(client):
    """User cannot edit another user's profile"""
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
    """User cannot delete another user's profile"""
    logout(client)
    login(client, 'username3','password3')
    before = client.get('/users/username1/')
    assert  b"username1" in before.data

    rv = client.get('/users/username1/delete', follow_redirects = True)

    assert b'You don&#39;t have permission to modify this profile' in rv.data
    logout(client)

def test_not_logged_in_cannot_edit_user_profile(client):
    """Cannot edit user profile if not logged in"""
    logout(client)
    before = client.get('/users/username1/')
    assert  b"username1" in before.data

    rv = client.post('/users/username1/edit',
            data = dict(name='new name for test',
                        text='Ugly text for test sdhsdjherj3eh12k;op'), follow_redirects = True)

    assert b'You don&#39;t have permission to modify this profile' in rv.data
    logout(client)

def test_not_logged_in_cannot_delete_user_profile(client):
    """Cannot delete user if not logged in"""
    logout(client)
    before = client.get('/users/username1/')
    assert  b"username1" in before.data
    rv = client.get('/users/username1/delete', follow_redirects = True)

    assert b'You don&#39;t have permission to modify this profile' in rv.data
    logout(client)

def test_cannot_see_users_list_if_not_logged_in(client):
    """Cannot see users list if not logged in"""
    logout(client)
    rv = client.get('/users', follow_redirects = True)
    assert  b"Only admin has access to this page" in rv.data

def test_cannot_see_users_list_if_logged_in_but_not_admin(client):
    """Cannot see users list if logged in but not admin"""
    login(client, 'username1','password1')
    rv = client.get('/users', follow_redirects = True)
    assert  b"Only admin has access to this page" in rv.data

def test_can_access_users_list_if_logged_in_as_admin(client):
    """Can access users list if logged in as admin"""
    login(client, 'admin','admin')
    rv = client.get('/users', follow_redirects = True)
    assert  b"Only admin has access to this page" not in rv.data
