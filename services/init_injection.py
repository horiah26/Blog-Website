"""Handles injection preparation for flask app"""
from repos.post import post_repo_db
from repos.post import post_repo_alchemy
from repos.post import post_repo_memory
from repos.user import user_repo_db
from repos.user import user_repo_alchemy
from repos.user import user_repo_memory
from repos.user import seed as user_seed
from repos.post import image_repo
from database import database
from services import auth
from config import config
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth as bp_auth
from blueprints.decorators import setup_requirements
from blueprints.decorators import permission_required
from blueprints.decorators import admin_required
from blueprints.decorators import login_required
from blueprints.decorators import edit_required_once
from blueprints.decorators import redirect_to_setup

from containers.container_db import ContainerDB
from containers.container_memory import ContainerMemory
from containers.container_alchemy import ContainerAlchemy


import app

class InitInjection():
    """Handles injection preparation for flask app"""
    def __init__(self, database_type):
        if database_type == 'db':
            self.container = ContainerDB()
        elif database_type == 'memory':
            self.container = ContainerMemory()
        elif database_type == 'alchemy':
            self.container = ContainerAlchemy()
        else:
            print('DB_TYPE not valid. Must be \'db\', \'alchemy\' or \'memory\'')

        self.container.wire(modules = [app,
                                        post_repo_db,
                                        user_repo_db,
                                        database,
                                        setup,
                                        blog,
                                        auth,
                                        bp_auth,
                                        admin_required,
                                        setup_requirements,
                                        permission_required,
                                        login_required,
                                        users,
                                        post_repo_alchemy,
                                        user_repo_alchemy,
                                        user_seed,
                                        redirect_to_setup,
                                        edit_required_once,
                                        post_repo_memory,
                                        user_repo_memory,
                                        config,
                                        image_repo])

    def get_container(self):
        """Returns container"""
        return self.container
