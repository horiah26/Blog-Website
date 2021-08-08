"""Container for password hash"""
from dependency_injector import containers, providers
    
from database.hash_imported_passwords import HashImportedPasswords

class PasswordContainer(containers.DeclarativeContainer):
    """Container for password hash"""

    password_hash_factory = providers.Factory(
        HashImportedPasswords
    )