"""Post tests"""
import datetime
from unittest import mock
from conftest import login, logout

def test_homepage_works(client):
    """Tests if homepage works"""
    rv = client.get('/')
    assert b'blog-description' in rv.data
    assert b'wrapper' in rv.data
    assert b'welcome' in rv.data
    assert b'category-tag popular' in rv.data
    assert b'profile-img' in rv.data

def test_display_name_not_username_shown_in_main_cards(client):
    """Does not update an article if the input is an empty title"""
    rv = client.get('/')
    assert b' <h6 class="owner">\n                            Name 2\n                        </h6>' in rv.data

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

def test_shows_posts_on_user_profile(client):
    """Can open the last post from seed"""
    rv = client.get('/users/username1/')
    print (rv.data)
    assert b'Duis a lectus in erat blandit hendrerit ' in rv.data

def test_redirects_if_post_not_found(client):
    """Redirects if post at index not found"""
    assert b'Post not found' in client.get('/100/', follow_redirects=True).data

def test_can_log_in_user_redirects_to_homepage(client):
    """Tests if page is rediected after log in"""
    login = client.post('/login',
                data = dict(username='username3',
                    password = 'password3'), follow_redirects=True)

    assert login.status_code == 200

    assert b'blog-description' in login.data
    assert b'wrapper' in login.data
    assert b'welcome' in login.data

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

def test_write_article(client):
    """Writes a new article"""
    login(client, 'username1', 'password1')

    client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    newpost = client.get('/9/').data #8 posts in seed

    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost

    logout(client)

def test_does_not_write_article_with_empty_text(client):
    """Does not write article with empty text"""
    login(client, 'username1', 'password1')

    assert client.get('/9/').status_code == 200 #post 9 exists (8 from seed + 1 created previously)
    assert b'Post not found' in client.get('/10/', follow_redirects=True).data #post 10 does not exist

    client.post('/create',
            data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                        text=' '), follow_redirects=True)

    assert b'Post not found' in client.get('/10/', follow_redirects=True).data

def test_does_not_write_article_with_empty_title(client):
    """Does not write article with empty title"""
    login(client, 'username1', 'password1')

    assert client.get('/9/').status_code == 200 #post 9 exists (8 from seed + 1 created previously))
    assert b'Post not found' in client.get('/10/', follow_redirects=True).data #post 11 does not exist

    rv = client.post('/create',
                data = dict(title=' ',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))
    assert b'Title is required' in rv.data
    assert b'Post not found' in client.get('/10/', follow_redirects=True).data

def test_admin_can_delete_other_users_post(client):
    """Can delete post"""
    login(client, 'admin', 'admin')
    assert client.get('/7/').status_code == 200

    client.get('/7/delete')
    print(client.get('/7/', follow_redirects=True).data)
    assert b'Post not found' in client.get('/7/', follow_redirects=True).data
    logout(client)

def test_can_update_post(client):
    """Can update post"""
    logout(client)
    login(client, 'username1', 'password1')

    data = dict(title = 'Ugly title for test lsdkhnsdpbjeri21', text = 'Ugly text for test asfjkoas.fnklwpgow[gp[g161;pq')

    rv = client.post('/2/update', data=data, follow_redirects=True)
    assert b'Post has been updated' in rv.data
    rv2 = client.get('/2/')
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
    login(client, 'admin', 'admin')
    assert client.get('/6/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/6/', follow_redirects=True).data
    assert client.get('/5/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/5/', follow_redirects=True).data
    assert client.get('/8/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/8/', follow_redirects=True).data
    assert client.get('/1/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/1/', follow_redirects=True).data
    assert client.get('/2/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/12/', follow_redirects=True).data
    assert client.get('/4/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/4/', follow_redirects=True).data
    assert client.get('/9/delete', follow_redirects=True).status_code == 200
    assert b'Post not found' in client.get('/9/', follow_redirects=True).data

    assert b'Post not found' in client.get('/1/', follow_redirects=True).data
    assert b'Post not found' in client.get('/10/', follow_redirects=True).data

    client.post('/create',
                    data=dict(title='Ugly title for test lsdkhnsdpbjeri',
                    text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'), follow_redirects = True)

    newpost = client.get('/1/')
    assert newpost.status_code == 200

    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost.data
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost.data

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
