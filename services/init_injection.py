"""Handles injection preparation for flask app"""
from blueprints import setup, users, blog, api, auth as bp_auth
from blueprints.decorators import setup_requirements, permission_required, admin_required, login_required, edit_required_once, redirect_to_setup
from repos.post import post_repo_db, post_repo_alchemy, post_repo_memory, image_repo
from repos.user import user_repo_db, user_repo_alchemy, user_repo_memory, seed as user_seed
from database import database
from services import auth, statistics
from config import config

from containers.container_db import ContainerDB
from containers.container_memory import ContainerMemory
from containers.container_alchemy import ContainerAlchemy

import app

class InitInjection:
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

        self.container.wire(modules=[app,
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
                                     image_repo,
                                     statistics,
                                     api])

    def get_container(self):
        """Returns container"""
        return self.container
