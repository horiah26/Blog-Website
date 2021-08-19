"""General purpose container"""
from dependency_injector import containers, providers

from config.config_db import ConfigDB
from config.config import Config
from config.alchemy_url import AlchURL
from database.database import Database
from services.auth import Authentication
from services.hasher import Hasher
from services.statistics import Statistics

from repos.post.post_repo_alchemy import RepoPostsAlchemy
from repos.post.seed import get as post_seed
from repos.post.image_repo import ImageRepo

from repos.user.user_repo_alchemy import RepoUserAlchemy
from repos.user.seed import get as user_seed

class ContainerAlchemy(containers.DeclarativeContainer):
    """General purpose container"""

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

    alch_url = providers.Factory(
        AlchURL,
        config_db = config_db
    )

    img_repo = providers.Singleton(
        ImageRepo
    )

    post_repo = providers.Singleton(
        RepoPostsAlchemy,
        config = config,
        seed = post_seed(),
        alch_url = alch_url
    )

    user_repo = providers.Singleton(
        RepoUserAlchemy,
        config = config,
        seed = user_seed(),
        alch_url = alch_url
    )

    auth = providers.Factory(
        Authentication,
        user_repo = user_repo
    )

    database = providers.Factory(
        Database,
        config = config,
        config_db = config_db
    )

    statistics = providers.Factory(
        Statistics,
        post_repo = post_repo)
