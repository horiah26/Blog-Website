from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

from repos.post.IPostRepo import IPostRepo
from repos.post.post_repo_db import RepoPostsDB 
from repos.post.post_repo_memory import RepoPostsMemory 
from repos.post.post_repo_alchemy import RepoPostsAlchemy
from repos.post.seed import get as post_seed
    
from repos.user.IUserRepo import IUserRepo
from repos.user.user_repo_db import RepoUserDB
from repos.user.user_repo_memory import RepoUserMemory
from repos.user.user_repo_alchemy import RepoUserAlchemy
from repos.user.seed import get as user_seed

class RepoContainer(containers.DeclarativeContainer):
   
    post_repo_db_factory = providers.Singleton(
        RepoPostsDB,
        seed = post_seed()
    )    

    post_repo_memory_factory = providers.Singleton(
        RepoPostsMemory,
        seed = post_seed()
    )      

    post_repo_alchemy_factory = providers.Singleton(
        RepoPostsAlchemy,
        seed = post_seed()
    )    

    user_repo_db_factory = providers.Singleton(
        RepoUserDB,
        seed = user_seed()
    )        

    user_repo_memory_factory = providers.Singleton(
        RepoUserMemory,
        seed = user_seed()
    )      
    
    user_repo_alchemy_factory = providers.Singleton(
        RepoUserAlchemy,
        seed = user_seed()
    )        