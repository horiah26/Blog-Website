from flaskr import create_app
from flaskr.db import init_db_command



if __name__ == '__main__':
    app = create_app()
    app.run()