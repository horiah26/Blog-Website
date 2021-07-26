"""Post tests"""
import datetime
from unittest import mock
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

def test_homepage_works(client):
    """Tests if homepage works"""
    rv = client.get('/')
    assert b'blog-description' in rv.data
    assert b'wrapper' in rv.data
    assert b'welcome' in rv.data
    assert b'category-tag popular' in rv.data
    assert b'profile-img' in rv.data

def test_shows_date_correctly(client):
    """Tests the date is shown correctly"""
    rv = client.get('/1/')
    time_now = datetime.datetime.now().strftime("%B %d %Y")

    assert bytes(time_now, 'utf-8') in rv.data

def test_opens_first_post_from_seed(client):
    """Can open the first post from seed"""
    rv = client.get('/1/')
    assert b'view-post' in rv.data
    assert b'view-post-controls' in rv.data
    assert b'edit-delete' in rv.data
    assert b'view_post_text' in rv.data
    assert b'view-post-date' in rv.data
    assert b'Suspendisse dui elit' in rv.data

    time_now = datetime.datetime.now().strftime("%B %d %Y")

    assert bytes(time_now, 'utf-8') in rv.data

def test_opens_last_post_from_seed(client):
    """Can open the last post from seed"""
    rv = client.get('/8/')
    assert b'view-post' in rv.data
    assert b'view-post-controls' in rv.data
    assert b'edit-delete' in rv.data
    assert b'view_post_text' in rv.data
    assert b'view-post-date' in rv.data
    assert b'Donec tincidunt maximus sem' in rv.data

def test_error404_nonexistent_post(client):
    """Returns 404 if post at index not found"""
    assert client.get('/100/').status_code == 404

def test_can_log_in_user_redirects_to_homepage(client):
    """Tests if page is rediected after log in"""
    login = client.post('/login',
                data = dict(username='username3',
                    password = 'password3'), follow_redirects=True)

    assert login.status_code == 200

    assert b'blog-description' in login.data
    assert b'wrapper' in login.data
    assert b'welcome' in login.data

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

def admin_can_update_post(client):
    """Can update post"""
    rv = login(client, 'admin', 'admin')

    data = dict(title = 'Ugly title for test lsdkhnsdpbjeri', text = 'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq')

    rv = client.post('/6/update', data=data, follow_redirects=True)

    assert b'Post has been updated' in rv.data

    rv2 = client.get('/6/')

    assert b'Ugly title for test lsdkhnsdpbjeri' in rv2.data
    assert b'Ugly text for test asfjkoas' in rv2.data

    logout(client)

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

def test_write_article(client):
    """Writes a new article"""
    login(client, 'username1', 'password1')

    client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    newpost = client.get('/10/').data #9 posts in seed

    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost

    logout(client)

def test_does_not_write_article_with_empty_text(client):
    """Does not write article with empty text"""
    login(client, 'username1', 'password1')

    assert client.get('/10/').status_code == 200 #post 10 exists (9 from seed + 1 created previously)
    assert client.get('/11/').status_code == 404 #post 11 does not exist

    client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text=' '))

    assert client.get('/11/').status_code == 404

def test_does_not_write_article_with_empty_title(client):
    """Does not write article with empty title"""
    login(client, 'username1', 'password1')

    assert client.get('/10/').status_code == 200 #post 10 exists (9 from seed + 1 created previously))
    assert client.get('/11/').status_code == 404 #post 11 does not exist

    rv = client.post('/create',
                data = dict(title=' ',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))
    assert b'Title is required' in rv.data
    assert client.get('/11/').status_code == 404

def test_cannot_delete_post_if_not_logged_in(client):
    """Can delete post"""
    logout(client)
    assert client.get('/3/').status_code == 200

    rv = client.get('/3/delete', follow_redirects=True)
    print(rv.data)
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

    assert client.get('/3/').status_code == 404
    logout(client)

def test_admin_can_delete_other_users_post(client):
    """Can delete post"""
    login(client, 'admin', 'admin')
    assert client.get('/7/').status_code == 200

    client.get('/7/delete')

    assert client.get('/7/').status_code == 404
    logout(client)

def test_can_update_post(client):
    """Can update post"""
    rv = login(client, 'username2', 'password2')

    data = dict(title = 'Ugly title for test lsdkhnsdpbjeri', text = 'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq')

    rv = client.post('/5/update', data=data, follow_redirects=True)
    assert b'Post has been updated' in rv.data
    rv2 = client.get('/5/')
    assert b'Ugly title for test lsdkhnsdpbjeri' in rv2.data
    assert b'Ugly text for test asfjkoas' in rv2.data

    logout(client)

def test_does_not_update_article_with_empty_text(client):
    """Does not update an article if the input is an empty text"""
    login(client, 'username1', 'password1')
    before = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in before.data
    client.post('/4/update',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text=' '), follow_redirects = True)
    after = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in after.data
    assert  b"<title>\nUgly title for test lsdkhnsdpbjeri\n</title>" not in after.data

    logout(client)

def test_does_not_update_article_with_empty_title(client):
    """Does not update an article if the input is an empty title"""
    before = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in before.data
    rv = client.post('/4/update',
                     data = dict(title=' ',
                                 text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'), follow_redirects = True)
    assert rv.status_code == 200
    after = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in after.data
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' not in after.data

def test_can_delete_all_posts_then_create_new_one_at_index1(client):
    """Deletes all posts then creates a new one"""
    login(client, 'username1', 'password1')
    assert client.get('/1/delete', follow_redirects=True).status_code == 200
    assert client.get('/1/').status_code == 404
    assert client.get('/2/delete', follow_redirects=True).status_code == 200
    assert client.get('/2/').status_code == 404
    assert client.get('/4/delete', follow_redirects=True).status_code == 200
    assert client.get('/4/').status_code == 404

    assert client.get('/9/delete', follow_redirects=True).status_code == 200
    assert client.get('/9/').status_code == 404
    logout(client)

    login(client, 'username2', 'password2')
    assert client.get('/5/delete', follow_redirects=True).status_code == 200
    assert client.get('/5/').status_code == 404
    assert client.get('/6/delete', follow_redirects=True).status_code == 200
    assert client.get('/6/').status_code == 404
    assert client.get('/8/delete', follow_redirects=True).status_code == 200
    assert client.get('/8/').status_code == 404

    assert client.get('/1/').status_code == 404
    assert client.get('/9/').status_code == 404
    assert client.get('/10/').status_code == 404

    login(client, 'username2', 'password2')

    client.post('/create',
                    data=dict(title='Ugly title for test lsdkhnsdpbjeri',
                    text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'), follow_redirects = True)

    newpost = client.get('/1/')
    assert newpost.status_code == 200

    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost.data
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost.data

def test_admin_can_edit_another_user_profile(client):
    """Does not update an article if the input is an empty title"""
    logout(client)
    login(client, 'admin','admin')
    before = client.get('/users/username1/')
    assert  b"username1" in before.data

    client.post('/users/username1/edit',
            data = dict(name='new name for test',
                        email='Ugly text for test sdhsdjherj3eh12k;op'), follow_redirects = True)

    after = client.get('/users/username1/')
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

def test_display_name_not_username_shown_in_main_cards(client):
    """Does not update an article if the input is an empty title"""
    rv = client.get('/')
    assert  b"username2" not in rv.data
    assert b'Name 2'in rv.data

@mock.patch("config.config_db.ConfigDB.config_file_exists", return_value = False)
def test_homepage_redirects_to_setup_if_no_db_config(mock_check, client):
    """Tests if homepage redirects if no db_config"""
    redirected = client.get('/', follow_redirects=True)
    assert b'blog-description' not in redirected.data
    assert b'wrapper' not in redirected.data
    assert b'welcome' not in redirected.data

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config_db.ConfigDB.config_file_exists", return_value = False)
def test_create_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if /create redirects if no db_config"""
    redirected = client.get('/create', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config_db.ConfigDB.config_file_exists", return_value = False)
def test_update_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if /update redirects if no db_config"""
    redirected = client.get('/1/update', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config_db.ConfigDB.config_file_exists", return_value = False)
def test_index_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/1/', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data
