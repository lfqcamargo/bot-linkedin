from src.models.postgres.settings.connection import db_connection_handler
from src.controllers.update_user_controller import UpdateUserController
from src.models.postgres.repositories.users_repository import UsersRepository

def update_user_composer():
    users_respotiory = UsersRepository(db_connection_handler)
    controller = UpdateUserController(users_respotiory)
    
    return controller 