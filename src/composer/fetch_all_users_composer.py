
from src.models.postgres.settings.connection import db_connection_handler
from src.controllers.fetch_all_users_controller import FetchAllUsersController
from src.models.postgres.repositories.users_repository import UsersRepository


def fetch_all_users_composer():
    users_respotiory = UsersRepository(db_connection_handler)
    controller = FetchAllUsersController(users_respotiory)

    return controller