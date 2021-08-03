from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

from database.database import Database

class DBContainer(containers.DeclarativeContainer):
    
    database_factory = providers.Factory(
        Database
    )

