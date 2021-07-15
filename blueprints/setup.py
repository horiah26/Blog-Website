"""Route to setting up database"""
import json
from flask import (
    Blueprint, redirect, render_template, request, url_for
)

bp = Blueprint('setup', __name__)

@bp.route('/setup', methods=['GET', 'POST'])
def setup_db():
    """Route to setting up database"""
    if request.method == 'POST':
        database = request.form['database'].strip()
        user = request.form['user'].strip()
        password = request.form['password'].strip()
        host = request.form['host'].strip()

        data = {
           "database" : database,
           "user" : user,
           "password" : password,
           "host": host
            }

        with open('database/db_config.json', 'w') as file:
            json.dump(data, file)

        return redirect(url_for('blog.home'))
    return render_template('database/setup.html')
