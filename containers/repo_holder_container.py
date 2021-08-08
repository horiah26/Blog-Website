"""Container for repo holders"""
from dependency_injector import containers, providers

from models.post_repo_holder import PostRepoHolder
from models.user_repo_holder import UserRepoHolder

class RepoHolderContainer(containers.DeclarativeContainer):
    """Container for repo holders"""

    post_repo_holder_factory = providers.Singleton(
        PostRepoHolder
    )

    user_repo_holder_factory = providers.Singleton(
        UserRepoHolder
    )
