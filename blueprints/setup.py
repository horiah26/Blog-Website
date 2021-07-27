"""Route to setting up database"""
from flask import (
    Blueprint, redirect, render_template, flash, request, url_for
)
from models.db_auth import DbAuth
from database.database import Database
from config.config_db import ConfigDB

bp = Blueprint('setup', __name__)
config = ConfigDB()

@bp.route('/setup', methods=['GET', 'POST'])
def setup_db():
    """Route to setting up database"""
    if request.method == 'POST':
        database = request.form['database'].strip()
        user = request.form['user'].strip()
        password = request.form['password'].strip()
        host = request.form['host'].strip()

        db_auth = DbAuth(database, host, user, password)
        config.save(db_auth.json)
        Database().create_update_tables()
        flash("Database has been set up")
        return redirect(url_for('blog.home'))
    return render_template('database/setup.html')
