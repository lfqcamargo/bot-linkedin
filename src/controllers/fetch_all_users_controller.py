import base64
from src.models.postgres.entities.user import User
from src.models.postgres.interfaces.users_repository_interface import UsersRepositoryInterface


class FetchAllUsersController:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self.users_repository = users_repository

    def handle(self) -> list[dict]:
        users = self.users_repository.fetch_all()

        if not users:
            return []

        return self.__format_response(users)

    def __format_response(self, users: list[User]) -> list[dict]:
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "birthday_date": str(user.birthday_date),                
                "phone": user.phone,
                "curriculum": base64.b64encode(user.curriculum).decode('utf-8'),
            }
            for user in users
        ]
