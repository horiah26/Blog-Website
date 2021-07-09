from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import datetime


from repos.list import post_list as posts
from models.post import Post

bp = Blueprint('blog', __name__)

@bp.route('/')
def home():
    return render_template('blog/home.html', posts=posts)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']        
        error = None

        if not title:
            error = "Title is required"
        if not text:
            error = "Text is required"
        if error is not None:
            flash(error)
        else:
            time_now = datetime.datetime.now().strftime("Created at: %d/%m/%Y %H:%M:%S")
            if(len(posts) == 0):
                id = 1
            else:                
                id = max(post.id for post in posts) + 1 
            posts.append(Post(id, title, text, "admin", time_now, time_now))

            return redirect(url_for('blog.home'))
    
    return render_template('blog/create_post.html')

@bp.route('/<int:id>/', methods=('GET', 'SET'))
def show(id):
    return render_template('blog/show_post.html', post=get_post(id))

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if not title:
            title = post.title
        if not text:
            text = post.text
        else:
            post.title = title
            post.text = text
            post.date_modified = datetime.datetime.now().strftime("Last edited at: %d/%m/%Y %H:%M:%S")

            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    for i, post in enumerate(posts):
        if post.id == id:
            del posts[i]
            break
    return redirect(url_for('blog.home'))

def get_post(id):
    post = next((post for post in posts if post.id == id), None)

    if post is not None:
        return post