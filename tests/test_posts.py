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

def test_write_article(client):
    """Writes a new article"""
    client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    newpost = client.get('/9/').data #8 posts in seed

    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost

def test_does_not_write_article_with_empty_text(client):
    """Does not write article with empty text"""
    assert client.get('/9/').status_code == 200 #post 9 exists (8 from seed + 1 created previously)
    assert client.get('/10/').status_code == 404 #post 10 does not exist

    client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text=' '))

    assert client.get('/10/').status_code == 404

def test_does_not_write_article_with_empty_title(client):
    """Does not write article with empty title"""
    assert client.get('/9/').status_code == 200 #post 9 exists (8 from seed + 1 created previously)
    assert client.get('/10/').status_code == 404 #post 10 does not exist

    client.post('/create',
                data = dict(title=' ',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    assert client.get('/10/').status_code == 404

def test_can_delete_post(client):
    """Can delete post"""
    assert client.get('/3/').status_code == 200

    client.get('/3/delete')

    assert client.get('/3/').status_code == 404

def test_can_update_post(client):
    """Can update post"""
    data = dict(title = 'Ugly title for test lsdkhnsdpbjeri', text = 'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq')

    client.post('/5/update', data=data, follow_redirects=True)

    rv = client.get('/5/')

    assert b'Ugly title for test lsdkhnsdpbjeri' in rv.data
    assert b'Ugly text for test asfjkoas' in rv.data

def test_does_not_update_article_with_empty_text(client):
    """Does not update an article if the input is an empty text"""
    before = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in before.data
    rv = client.post('/4/update',
                     data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                                 text=' '))
    assert rv.status_code == 200
    after = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in after.data

def test_does_not_update_article_with_empty_title(client):
    """Does not update an article if the input is an empty title"""
    before = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in before.data
    rv = client.post('/4/update',
                     data = dict(title=' ',
                                 text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))
    assert rv.status_code == 200
    after = client.get('/4/')
    assert  b"<title>\nDuis a lectus\n</title>" in after.data

def test_can_delete_all_posts_then_create_new_one_at_index1(client):
    """Deletes all posts then creates a new one"""
    client.get('/1/delete')
    client.get('/2/delete')
    client.get('/3/delete')
    client.get('/4/delete')
    client.get('/5/delete')
    client.get('/6/delete')
    client.get('/7/delete')
    client.get('/8/delete')
    client.get('/9/delete')

    assert client.get('/1/').status_code == 404
    assert client.get('/10/').status_code == 404

    client.post('/create',
                    data=dict(title='Ugly title for test lsdkhnsdpbjeri',
                    text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    newpost = client.get('/1/').data

    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost

@mock.patch("database.connection.Connection.db_config_exists", return_value = False)
def test_homepage_redirects_to_setup_if_no_db_config(mock_db_config_exists, client):
    """Tests if homepage redirects if no db_config"""
    redirected = client.get('/', follow_redirects=True)
    assert b'blog-description' not in redirected.data
    assert b'wrapper' not in redirected.data
    assert b'welcome' not in redirected.data

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("database.connection.Connection.db_config_exists", return_value = False)
def test_create_redirects_to_setup_if_no_db_config(mock_db_config_exists, client):
    """Tests if /create redirects if no db_config"""
    redirected = client.get('/create', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("database.connection.Connection.db_config_exists", return_value = False)
def test_update_redirects_to_setup_if_no_db_config(mock_db_config_exists, client):
    """Tests if /update redirects if no db_config"""
    redirected = client.get('/1/update', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("database.connection.Connection.db_config_exists", return_value = False)
def test_index_redirects_to_setup_if_no_db_config(mock_db_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/1/update', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data
