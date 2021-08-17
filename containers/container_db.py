"""Database container"""
from dependency_injector import containers, providers

from config.config_db import ConfigDB
from config.config import Config
from database.database import Database
from services.auth import Authentication
from services.hasher import Hasher

from repos.post.post_repo_db import RepoPostsDB
from repos.post.seed import get as post_seed
from repos.post.image_repo import ImageRepo

from repos.user.user_repo_db import RepoUserDB
from repos.user.seed import get as user_seed

class ContainerDB(containers.DeclarativeContainer):
    """Database container"""

    config = providers.Configuration()

    hasher = providers.Factory(
        Hasher
    )

    config_db = providers.Factory(
        ConfigDB
    )

    config = providers.Factory(
        Config
    )

    img_repo = providers.Singleton(
        ImageRepo
    )

    database = providers.Factory(
        Database,
        config = config,
        config_db = config_db
    )

    post_repo = providers.Singleton(
        RepoPostsDB,
        db = database,
        seed = post_seed()
    )

    user_repo = providers.Singleton(
        RepoUserDB,
        db = database,
        seed = user_seed()
    )

    auth = providers.Factory(
        Authentication,
        user_repo = user_repo
    )
