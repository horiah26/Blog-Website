from flask import Flask

def create_app():
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret")  

    import blueprints.blog as blog
    app.register_blueprint(blog.bp)
    return app

app = create_app()
app.run(debug=True)