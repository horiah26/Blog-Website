from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from repositories.list import post_list as posts

bp = Blueprint('blog', __name__)
@bp.route('/')
def index():
    return render_template('posts.html', posts=posts)