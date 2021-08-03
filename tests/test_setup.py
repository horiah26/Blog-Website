"""Setup tests"""
from unittest import mock
@mock.patch("config.config.Config.config_file_exists", return_value = False)
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

@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_create_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if /create redirects if no db_config"""
    redirected = client.get('/create', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_update_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if /update redirects if no db_config"""
    redirected = client.get('/1/update', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_post_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/1/', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_user_profile_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/users/username2/', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_login_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/login', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data

@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_signup_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/signup', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data


@mock.patch("config.config.Config.config_file_exists", return_value = False)
def test_edit_required_redirects_to_setup_if_no_db_config(mock_config_exists, client):
    """Tests if article at index redirects if no db_config"""
    redirected = client.get('/users/username1/edit_required', follow_redirects=True)

    assert b'<label class="crud_label" for="database"> Database </label> <br>' in redirected.data
    assert b'<input type="text" class="form-title" name="database"><br>' in redirected.data
    assert b'<input type="password" class="form-title" name="password"><br>' in redirected.data
    assert b'<input type="submit" value="Submit">' in redirected.data
