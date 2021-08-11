"""General purpose container"""
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
    
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config_db import ConfigDB
from config.config import Config
from database.database import Database
from services.auth import Authentication
from database.hash_imported_passwords import HashImportedPasswords

from config.alchemy_url import AlchURL

from repos.post.post_repo_db import RepoPostsDB
from repos.post.post_repo_memory import RepoPostsMemory
from repos.post.post_repo_alchemy import RepoPostsAlchemy
from repos.post.seed import get as post_seed

from repos.user.user_repo_db import RepoUserDB
from repos.user.user_repo_memory import RepoUserMemory
from repos.user.user_repo_alchemy import RepoUserAlchemy
from repos.user.seed import get as user_seed

from models.post_repo_holder import PostRepoHolder
from models.user_repo_holder import UserRepoHolder

class Container(containers.DeclarativeContainer):
    """General purpose container"""

    config = providers.Configuration()

    config_db = providers.Factory(
        ConfigDB
    )

    config = providers.Factory(
        Config
    )

    database = providers.Factory(
        Database
    )
    
    auth = providers.Factory(
        Authentication
    )
    
    password_hash = providers.Factory(
        HashImportedPasswords
    )

    alch_url = providers.Factory(
        AlchURL
    )

    post_repo_db = providers.Singleton(
        RepoPostsDB,
        seed = post_seed()
    )

    post_repo_memory = providers.Singleton(
        RepoPostsMemory,
        seed = post_seed()
    )

    post_repo_alchemy = providers.Singleton(
        RepoPostsAlchemy,
        seed = post_seed()
    )

    user_repo_db = providers.Singleton(
        RepoUserDB,
        seed = user_seed()
    )

    user_repo_memory = providers.Singleton(
        RepoUserMemory,
        seed = user_seed()
    )

    user_repo_alchemy = providers.Singleton(
        RepoUserAlchemy,
        seed = user_seed()
    )
    
    post_repo_holder = providers.Singleton(
        PostRepoHolder
    )

    user_repo_holder = providers.Singleton(
        UserRepoHolder
    )