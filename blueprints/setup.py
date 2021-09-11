"""Route to setting up database"""
from flask import (
    Blueprint, redirect, render_template, flash, request, url_for
)
from dependency_injector.wiring import inject, Provide
from models.db_auth import DbAuth
from blueprints.decorators.setup_requirements import setup_requirements

bp = Blueprint('setup', __name__)


@bp.route('/setup', methods=['GET', 'POST'])
@setup_requirements
@inject
def setup_db(db=Provide['database'], config_db=Provide['config_db']):
    """Route to setting up database"""
    if request.method == 'POST':
        database = request.form['database'].strip()
        user = request.form['user'].strip()
        password = request.form['password'].strip()
        host = request.form['host'].strip()

        db_auth = DbAuth(database, host, user, password)
        config_db.save(db_auth)
        db.create_update_tables()
        flash("Database has been set up")
        return redirect(url_for('blog.home'))
    return render_template('database/setup.html')
