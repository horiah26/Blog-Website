"""General purpose container"""
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

from models.db_auth import DbAuth
from config.config_db import ConfigDB
from config.config import Config
from models.post import Post
from models.post_preview import PostPreview
from models.user import User

class Container(containers.DeclarativeContainer):
    """General purpose container"""
    config = providers.Configuration()

    db_auth_factory = providers.Factory(
        DbAuth
    )

    config_db_factory = providers.Factory(
        ConfigDB
    )

    config_factory = providers.Factory(
        Config
    )

    user_factory = providers.Factory(
        User
    )

    post_factory = providers.Factory(
        Post
    )

    preview_factory = providers.Factory(
        PostPreview
    )
