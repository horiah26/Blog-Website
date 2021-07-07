from flask import Flask
from models.post import Post
from repositories.list import post_list

def create_app():
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret")
    
    post1 = Post(1, "title", "text 1")
    post2 = Post(2, "title2", "text 2")
    post3 = Post(2, "title 3", "text 3")
    post4 = Post(2, "title 3", "text 3")

    post_list.append(post1)
    post_list.append(post2)

    import blog
    app.register_blueprint(blog.bp)

    return app

app = create_app()
app.run()