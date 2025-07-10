import pytest
from src.models.postgres.settings.connection import db_connection_handler
from src.models.postgres.entities.user import User
from src.models.postgres.entities.question import QuestionTypes
from src.models.postgres.repositories.questions_repository import QuestionsRepository
from src.services.gemini_service import generate_embeddings
from datetime import date

def test_created_question() -> None:
    with db_connection_handler as database:
        session = database.session
        
    session.query(User).delete()
        
    user = User(
            name="Lucas Fernando",
            email="lfqcamargo@gmail.com",
            password="123456",
            phone="14991396707",
            birthday_date=date.today(),
            curriculum=b"teste em bytes"
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    embeddings = generate_embeddings("Você tem conhecimentos em Python?")
    
    questions_repository = QuestionsRepository()
    result = questions_repository.create(
        user_id=user.id,
        question_type=QuestionTypes.TEXT,
        question="Você tem conhecimentos em Python?",
        embeddings=embeddings,
        response=None
    )
    
    print(result)
    
    assert result is not None