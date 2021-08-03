from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from services.auth import Authentication

class AuthContainer(containers.DeclarativeContainer):

    auth_factory = providers.Factory(
    Authentication
    )

