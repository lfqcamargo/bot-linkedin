from src.models.postgres.interfaces.users_repository_interface import UsersRepositoryInterface

class RunLinkedinBotController:
    def __init__(self, linkedin_service) -> None:
        self.linkedin_service = linkedin_service

    def handle(self, user_id: dict) -> None:
        if user_id is None:
            raise ValueError("ID do usuário é obrigatório para edição.")
        
        user_id = user_id["id"]
        self.linkedin_service.execute(user_id)
        
