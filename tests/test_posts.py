"""Post tests"""
import datetime
from conftest import login, logout

def test_homepage_works(client):
    """Tests if homepage works"""
    rv = client.get('/')
    assert b'blog-description' in rv.data
    assert b'wrapper' in rv.data
    assert b'welcome' in rv.data
    assert b'category-tag popular' in rv.data
    assert b'profile-img' in rv.data

def test_display_name_not_username_shown_in_cards(client):
    """Does display name is shown in cards"""
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

def test_shows_display_name_in_post_view(client):
    """Test shows display name in post view"""
    rv = client.get('/6/')
    print(rv.data)
    assert b'Name 2' in rv.data

def test_opens_last_post_from_seed(client):
    """Can open the last post from seed"""
    rv = client.get('/8/')
    assert b'view-post' in rv.data
    assert b'view-post-controls' in rv.data
    assert b'edit-delete' in rv.data
    assert b'view_post_text' in rv.data
    assert b'view-post-date' in rv.data
    assert b'Donec tincidunt maximus sem' in rv.data

def test_can_update_post(client):
    """Can update post"""
    logout(client)
    login(client, 'username1', 'password1')

    data = dict(title = 'Ugly title for test lsdkhnsdpbjeri21', text = 'Ugly text for test asfjkoas.fnklwpgow[gp[g161;pq')

    rv = client.post('/2/update', data=data, follow_redirects=True)
    print(rv.data)
    assert b'Post has been updated' in rv.data
    rv2 = client.get('/2/')
    assert b'Ugly title for test lsdkhnsdpbjeri' in rv2.data
    assert b'Ugly text for test asfjkoas' in rv2.data

    logout(client)

def test_redirects_if_post_not_found(client):
    """Redirects if post at index not found"""
    assert b'Post not found' in client.get('/100/', follow_redirects=True).data

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

    newpost = client.get('/15/').data #14 posts in seed
    print(newpost)
    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost

    logout(client)

def test_does_not_write_article_with_empty_text(client):
    """Does not write article with empty text"""
    login(client, 'username1', 'password1')

    assert client.get('/14/').status_code == 200
    assert b'Post not found' in client.get('/15/', follow_redirects=True).data

    rv = client.post('/create',
            data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                        text=' '), follow_redirects=True)

    assert b'Text is required' in rv.data

def test_does_not_write_article_with_empty_title(client):
    """Does not write article with empty title"""
    login(client, 'username1', 'password1')

    assert client.get('/14/').status_code == 200
    assert b'Post not found' in client.get('/15/', follow_redirects=True).data

    rv = client.post('/create',
                data = dict(title=' ',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))
    assert b'Title is required' in rv.data
    assert b'Post not found' in client.get('/15/', follow_redirects=True).data

def test_admin_can_delete_other_users_post(client):
    """Can delete other user's post"""
    login(client, 'admin', 'admin')
    assert client.get('/7/').status_code == 200

    client.get('/7/delete')
    print(client.get('/7/', follow_redirects=True).data)
    assert b'Post not found' in client.get('/7/', follow_redirects=True).data
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

def test_does_not_write_article_if_not_logged_in(client):
    """Cannot write article if not logged_in"""
    redirect = client.post('/create',
                data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                            text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'), follow_redirects=True)

    assert b'You must be logged in to do this' in redirect.data

def test_cannot_delete_post_if_not_logged_in(client):
    """Cannot delete post if not logged in"""
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
    """Can delete post if logged in"""
    login(client, 'username1', 'password1')
    assert client.get('/3/').status_code == 200

    client.get('/3/delete')
    print(client.get('/3/', follow_redirects=True).data)
    assert b'Post not found' in client.get('/3/', follow_redirects=True).data
    logout(client)

def test_paging_works(client):
    """Paging works"""
    rv = client.get('/?page=1')
    assert b'id="active-page">1</a>' in rv.data
    assert b'id="inactive-page">2</a>' in rv.data
    assert b'id="inactive-page">3</a>' in rv.data

    assert b'Vivamus pretium dui' in rv.data
    assert b'Nullam quis quam convallis' not in rv.data
    assert b'Lorem ipsum dolor sit amet, consectetur adipiscing elit' not in rv.data

    rv = client.get('/?page=2')
    assert b'id="inactive-page">1</a>' in rv.data
    assert b'id="active-page">2</a>' in rv.data
    assert b'id="inactive-page">3</a>' in rv.data

    assert b'Vivamus pretium dui' not in rv.data
    assert b'Nullam quis quam convallis' in rv.data
    assert b'Lorem ipsum dolor sit amet, consectetur adipiscing elit' not in rv.data

    rv = client.get('/?page=3')
    assert b'id="inactive-page">1</a>' in rv.data
    assert b'id="inactive-page">2</a>' in rv.data
    assert b'id="active-page">3</a>' in rv.data

    assert b'Vivamus pretium dui' not in rv.data
    assert b'Nullam quis quam convallis' not in rv.data
    assert b'Lorem ipsum dolor sit amet, consectetur adipiscing elit' in rv.data
