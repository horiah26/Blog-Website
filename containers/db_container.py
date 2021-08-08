"""Container for database container"""
from dependency_injector import containers, providers

from database.database import Database

class DBContainer(containers.DeclarativeContainer):
    """Container for authentication"""
    database_factory = providers.Factory(
        Database
    )

