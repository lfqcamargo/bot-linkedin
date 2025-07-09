from src.controllers.errors.validate_exception import ValidationException
from src.models.postgres.interfaces.users_repository_interface import UsersRepositoryInterface


class DeleteUserController:
    def __init__(self, user_repository: UsersRepositoryInterface):
        self.user_repository = user_repository

    def handle(self, props: dict) -> None:
        user_id = props.get("id")

        if user_id is None:
            raise ValidationException(f"Informe o ID do usuário.")

        self.user_repository.delete(user_id) 