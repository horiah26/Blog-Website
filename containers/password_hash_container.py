from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
    
from database.hash_imported_passwords import HashImportedPasswords

class PasswordContainer(containers.DeclarativeContainer):
    
    password_hash_factory = providers.Factory(
        HashImportedPasswords
    )