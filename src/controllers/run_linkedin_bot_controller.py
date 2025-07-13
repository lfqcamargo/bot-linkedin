from src.services.linkedin_service import LinkedinService


class RunLinkedinBotController:
    def __init__(self) -> None:
        self.__linkedin_service = LinkedinService()

    def handle(self, user_id: dict) -> None:
        if user_id is None:
            raise ValueError("ID do usuário é obrigatório para edição.")

        user_id = user_id["id"]
        self.__linkedin_service.execute(user_id)
