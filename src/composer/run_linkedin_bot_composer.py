from src.services.linkedin_service import LinkedinService
from src.controllers.run_linkedin_bot_controller import RunLinkedinBotController
from src.models.postgres.repositories.users_repository import UsersRepository
from src.models.postgres.settings.connection import db_connection_handler

def run_linkedin_bot_composer():
    users_repository = UsersRepository(db_connection_handler)
    linkedin_service = LinkedinService(users_repository)
    controller = RunLinkedinBotController(linkedin_service)
    
    return controller 