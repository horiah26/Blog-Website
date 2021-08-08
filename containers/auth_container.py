"""Container for authentication"""
from dependency_injector import containers, providers
from services.auth import Authentication

class AuthContainer(containers.DeclarativeContainer):
    """Container for authentication"""
    auth_factory = providers.Factory(
    Authentication
    )
