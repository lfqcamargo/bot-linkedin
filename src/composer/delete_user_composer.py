from src.controllers.delete_user_controller import DeleteUserController
from src.models.postgres.repositories.users_repository import UsersRepository
from src.models.postgres.settings.connection import db_connection_handler

def delete_user_composer():
    users_repository = UsersRepository(db_connection_handler)
    controller = DeleteUserController(users_repository)
    
    return controller 