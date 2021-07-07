from flask import Flask
from repositories.list import post_list

def create_app():
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret")
    


    import blog
    app.register_blueprint(blog.bp)

    return app

app = create_app()
app.run()