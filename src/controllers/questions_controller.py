from src.models.postgres.repositories.questions_repository import QuestionsRepository
from src.models.postgres.entities.question import Question


class QuestionsController:
    def __init__(self, questions_repository: QuestionsRepository):
        self.questions_repository = questions_repository

    def handle(self, user_id: int) -> list[dict]:
        questions = self.questions_repository.fetch_all_by_user(user_id)
        if not questions:
            return []
        return self.__format_response(questions)

    def __format_response(self, questions: list[Question]) -> list[dict]:
        return [
            {
                "id": q.id,
                "date_time": str(q.date_time),
                "question_type": (
                    q.question_type.value
                    if hasattr(q.question_type, "value")
                    else str(q.question_type)
                ),
                "question": q.question,
                "response": q.response,
            }
            for q in questions
        ]

    def create_question(
        self, user_id: int, question_type: str, question: str, response: str = None
    ):
        # Embeddings pode ser None para perguntas criadas manualmente
        return self.questions_repository.create(
            user_id=user_id,
            question_type=question_type,
            question=question,
            embeddings=[],
            response=response,
        )

    def update_question(
        self,
        question_id: int,
        user_id: int,
        question_type: str,
        question: str,
        response: str = None,
    ):
        return self.questions_repository.update(
            question_id=question_id,
            user_id=user_id,
            question_type=question_type,
            question=question,
            response=response,
        )

    def delete_question(self, question_id: int):
        return self.questions_repository.delete(question_id)
