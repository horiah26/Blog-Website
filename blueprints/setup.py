"""Route to setting up database"""
from flask import (
    Blueprint, redirect, render_template, flash, request, url_for
)
from blueprints.decorators.setup_requirements import setup_requirements
from containers.container import Container
from containers.db_container import DBContainer

container = Container()
config_db = container.config_db_factory()
db = DBContainer().database_factory()
bp = Blueprint('setup', __name__)

@bp.route('/setup', methods=['GET', 'POST'])
@setup_requirements
def setup_db():
    """Route to setting up database"""
    if request.method == 'POST':
        database = request.form['database'].strip()
        user = request.form['user'].strip()
        password = request.form['password'].strip()
        host = request.form['host'].strip()

        db_auth = container.db_auth_factory(database, host, user, password)
        config_db.save(db_auth)
        db.create_update_tables()
        flash("Database has been set up")
        return redirect(url_for('blog.home'))
    return render_template('database/setup.html')
