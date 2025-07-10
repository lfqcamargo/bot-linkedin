from src.models.postgres.settings.connection import db_connection_handler
from src.models.postgres.entities.question import Question, QuestionTypes

class QuestionsRepository:
    def __init__(self) -> None:
        self.__db_connection_handler = db_connection_handler
        
    def create(self, 
        user_id: int,
        question_type: QuestionTypes,
        question: str,
        embeddings: list,
        response: str | None,
    ) -> None:
        with self.__db_connection_handler as database:
            session = database.session
            question = Question(
                        user_id=user_id,
                        question_type=question_type,
                        question=question,
                        embeddings=embeddings,
                        response=response,    
                    )
            try:
                session.add(question)
                session.commit()
                session.refresh(question)
                return question
            except Exception as e:
                session.rollback()
                print(f"Error during question creation: {e}")
                raise RuntimeError(f"Erro ao criar usuário: {e}") from e
                