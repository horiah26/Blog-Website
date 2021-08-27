"""Blueprint for api"""
from flask import (
    Blueprint, jsonify, session, abort
)
from dependency_injector.wiring import inject, Provide

bp = Blueprint('api', __name__)

@bp.route('/api/post/<int:post_id>')
@inject
def show_post(post_id, post_repo = Provide['post_repo']):
    """Returns a jsonified dict that contains post data, logged user and display name"""
    post = post_repo.get(post_id)
    if post is None:
        return jsonify(dict())
    dictionary = post[0].get_dict()

    if 'username' in session:
        username = session['username']
    else:
        username = None

    dictionary['active_user'] = username
    dictionary['display_name'] = post[1]

    return jsonify(dictionary)
