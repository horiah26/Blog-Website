"""General purpose container"""
from dependency_injector import containers, providers

from config.config_db import ConfigDB
from config.config import Config

from database.database import Database
from services.auth import Authentication
from services.hasher import Hasher
from services.statistics import Statistics

from repos.post.post_repo_memory import RepoPostsMemory
from repos.post.seed import get as post_seed
from repos.post.image_repo_memory import ImageRepoMemory

from repos.user.user_repo_memory import RepoUserMemory
from repos.user.seed import get as user_seed

class ContainerMemory(containers.DeclarativeContainer):
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

    user_repo = providers.Singleton(
        RepoUserMemory,
        seed = user_seed()
    )

    img_repo = providers.Singleton(
        ImageRepoMemory
    )

    post_repo = providers.Singleton(
        RepoPostsMemory,
        seed = post_seed(),
        user_repo = user_repo
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
