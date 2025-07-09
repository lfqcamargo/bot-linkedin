
from src.models.postgres.settings.connection import db_connection_handler
from src.controllers.create_user_controller import CreateUserController
from src.models.postgres.repositories.users_repository import UsersRepository


def create_user_composer():
    users_respotiory = UsersRepository(db_connection_handler)
    controller = CreateUserController(users_respotiory)

    return controller