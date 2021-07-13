import pytest
import datetime
import gc

from app import create_app

@pytest.fixture(scope="function")
def client():
    app = create_app()
    yield app.test_client()
    
    gc.collect()

#def test_can_update_first_post(client):
#    data = dict(title = 'Ugly title for test lsdkhnsdpbjeri', text = 'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq')
       
#    update = client.post('/1/update', data=data, follow_redirects=True)
    
#    rv = client.get('/1/')

#    assert b'Ugly title for test lsdkhnsdpbjeri' in rv.data
#    assert b'Ugly text for test asfjkoas' in rv.data

def test_homepage_works(client):    
    rv = client.get('/')
    assert b'blog-description' in rv.data
    assert b'wrapper' in rv.data
    assert b'welcome' in rv.data
    assert b'category-tag popular' in rv.data
    assert b'profile-img' in rv.data

    del client    

def test_shows_date_correctly(client): 
    rv = client.get('/1/')
    time_now = datetime.datetime.now().strftime("%B %d %Y")    

    assert bytes(time_now, 'utf-8') in rv.data

def test_opens_first_post_from_seed(client):    
    rv = client.get('/1/')
    assert b'view-post' in rv.data
    assert b'view-post-controls' in rv.data
    assert b'edit-delete' in rv.data
    assert b'view_post_text' in rv.data
    assert b'view_post_date' in rv.data
    assert b'Suspendisse dui elit' in rv.data

    time_now = datetime.datetime.now().strftime("%B %d %Y")   

    assert b'July 13 2021' in rv.data
    
def test_opens_last_post_from_seed(client):    
    rv = client.get('/8/')
    assert b'view-post' in rv.data
    assert b'view-post-controls' in rv.data
    assert b'edit-delete' in rv.data
    assert b'view_post_text' in rv.data
    assert b'view_post_date' in rv.data
    assert b'Donec tincidunt maximus sem' in rv.data

def test_error404_nonexistent_post(client):    
    assert client.get('/100/').status_code == 404


def test_write_article(client):
    rv = client.post('/create', 
                     data = dict(title='Ugly title for test lsdkhnsdpbjeri',
                                 text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    newpost = client.get('/9/').data #8 posts in seed
    
    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost
    
    
def test_can_delete_first_post(client):
    before_delete = client.get('/1/')
    
    assert client.get('/1/').status_code == 200
    assert b'<title>\nLorem Ipsum\n</title>' in before_delete.data
    assert b'<p id="view_post_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit' in before_delete.data

    deleted = client.get('/1/delete')

    assert client.get('/1/').status_code == 404

def test_can_delete_all_posts_then_create_new_one(client):    
    deleted = client.get('/1/delete')
    deleted = client.get('/2/delete')
    deleted = client.get('/3/delete')
    deleted = client.get('/4/delete')
    deleted = client.get('/5/delete')
    deleted = client.get('/6/delete')
    deleted = client.get('/7/delete')
    deleted = client.get('/8/delete')

    client.get('/9/').status_code == 404

    rv = client.post('/create', 
                     data=dict(title='Ugly title for test lsdkhnsdpbjeri',
                     text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'))

    newpost = client.get('/9/').data
    
    assert b'Ugly title for test lsdkhnsdpbjeri' in newpost
    assert b'Ugly text for test asfjkoas.fnklwpgow[gp[g;pq' in newpost