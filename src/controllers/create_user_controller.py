import base64
from datetime import datetime
from src.controllers.errors.validate_exception import ValidationException
from src.models.postgres.entities.user import User
from src.models.postgres.interfaces.users_repository_interface import UsersRepositoryInterface

class CreateUserController:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self.users_repository = users_repository

    def handle(self, props: dict) -> dict:
        try:
            name = props["name"].strip()
            email = props["email"].strip()
            password = props["password"]
            birthday_date = props["birthday_date"].strip()
            phone = props["phone"].strip()
            curriculum = props["curriculum"]
        except KeyError as e:
            raise ValidationException(f"Campo ausente no formulário: {e}")

        self.__validate_form(name, email, password, birthday_date, phone, curriculum)
        user = self.__create_user(name, email, password, birthday_date, phone, curriculum)
        return self.__format_response(user)

    def __validate_form(
        self, name: str, email: str, password: str, birthday_date: str, phone: str, curriculum: bytes
    ) -> None:
        if not name or not email or not password:
            raise ValidationException("Por favor, preencha todos os campos obrigatórios.")

        try:
            datetime.strptime(birthday_date, "%Y-%m-%d")
        except ValueError:
            raise ValidationException("Data de nascimento inválida. Use o formato YYYY-MM-DD.")

        if not phone.isdigit():
            raise ValidationException("Telefone deve conter apenas números.")

        if not curriculum:
            raise ValidationException("Por favor, selecione um arquivo de currículo.")

    def __create_user(
        self, name: str, email: str, password: str, birthday_date: str, phone: str, curriculum: bytes
    ) -> User:
        birthday_date_formatted = datetime.strptime(birthday_date, "%Y-%m-%d").date()
        user = self.users_repository.create(
            name=name,
            email=email,
            password=password,
            birthday_date=birthday_date_formatted,
            curriculum=curriculum,
            phone=phone
        )
        if not user:
            raise ValidationException("Erro ao salvar usuário no banco de dados.")

        return user

    def __format_response(self, user: User) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "birthday_date": str(user.birthday_date),
            "curriculum": base64.b64encode(user.curriculum).decode('utf-8'),
            "phone": user.phone
        }
