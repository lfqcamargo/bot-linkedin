import pytest
from src.models.postgres.settings.connection import db_connection_handler
from src.models.postgres.entities.user import User
from src.models.postgres.entities.question import QuestionTypes
from src.models.postgres.repositories.questions_repository import QuestionsRepository
from src.services.gemini_service import GeminiService
from datetime import date


def test_created_question() -> None:
    with db_connection_handler as database:
        session = database.session

    user = session.query(User).first()
    gemini = GeminiService()
    # embeddings_question = gemini.generate_embeddings("Você tem conhecimentos em JavaScript?")

    questions_repository = QuestionsRepository()
    # result = questions_repository.create(
    #     user_id=user.id,
    #     question_type=QuestionTypes.TEXT,
    #     question="Você tem conhecimentos em JavaScript?",
    #     embeddings=embeddings_question,
    #     response=None
    # )

    # embeddings_question = gemini.generate_embeddings("Você tem conhecimentos em Python?")
    # result = questions_repository.create(
    #     user_id=user.id,
    #     question_type=QuestionTypes.TEXT,
    #     question="Você tem conhecimentos em Python?",
    #     embeddings=embeddings_question,
    #     response=None
    # )

    embeddings_question = gemini.generate_embeddings("Tem conhecimentos em JavaScript?")
    result = questions_repository.find_by_similarity(user.id, embeddings_question)

    print("Resultado da Busca foi: ", result.question if result else None)
