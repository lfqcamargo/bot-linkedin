from src.models.postgres.repositories.questions_repository import QuestionsRepository
from src.models.postgres.entities.question import Question, QuestionTypes


class QuestionsController:
    def __init__(self) -> None:
        self.questions_repository = QuestionsRepository()

    def fetch_all_by_user(self, user_id: int) -> list[Question]:
        questions = self.questions_repository.fetch_all_by_user(user_id)
        if not questions:
            return []
        return questions

    def create_question(
        self, user_id: int, question_type: str, question: str, response: str = None
    ):
        # Embeddings pode ser None para perguntas criadas manualmente
        return self.questions_repository.create(
            user_id=user_id,
            question_type=QuestionTypes(question_type),
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
    ) -> Question:
        return self.questions_repository.update(
            question_id=question_id,
            user_id=user_id,
            question_type=QuestionTypes(question_type),
            question=question,
            response=response,
        )

    def delete_question(self, question_id: int):
        return self.questions_repository.delete(question_id)
