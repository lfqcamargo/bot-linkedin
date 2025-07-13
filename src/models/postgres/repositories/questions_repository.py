from sqlalchemy import select, func, cast, literal_column
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from src.models.postgres.settings.connection import db_connection_handler
from src.models.postgres.entities.question import Question, QuestionTypes


class QuestionsRepository:
    def __init__(self) -> None:
        self.__db_connection_handler = db_connection_handler

    def create(
        self,
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

    def find_by_similarity(
        self, user_id: int, question_embeddings: list[float], threshold: float = 0.3
    ) -> Question | None:
        with self.__db_connection_handler as database:
            session = database.session
            try:
                distance_expr = Question.embeddings.l2_distance(
                    question_embeddings
                ).label("dist")

                stmt = (
                    select(Question, distance_expr)
                    .where(Question.user_id == user_id, distance_expr <= threshold)
                    .order_by(distance_expr)
                    .limit(1)
                )

                result = session.execute(stmt).first()

                if result:
                    question, dist = result
                    return question
                return None

            except Exception as e:
                print(f"Error during similarity search: {e}")
                raise RuntimeError(
                    f"Erro ao buscar perguntas por similaridade: {e}"
                ) from e

    def fetch_all_by_user(self, user_id: int) -> list[Question]:
        """Busca todas as perguntas de um usuário."""
        with self.__db_connection_handler as database:
            session = database.session
            try:
                stmt = select(Question).where(Question.user_id == user_id)
                result = session.execute(stmt).scalars().all()
                return result
            except Exception as e:
                print(f"Error during fetch_all_by_user: {e}")
                raise RuntimeError(f"Erro ao buscar perguntas do usuário: {e}") from e

    def update(
        self,
        question_id: int,
        user_id: int,
        question_type: str,
        question: str,
        response: str = None,
    ):
        with self.__db_connection_handler as database:
            session = database.session
            try:
                q = session.get(Question, question_id)
                if not q:
                    raise RuntimeError("Pergunta não encontrada.")
                q.user_id = user_id
                q.question_type = question_type
                q.question = question
                q.response = response
                session.commit()
                session.refresh(q)
                return q
            except Exception as e:
                session.rollback()
                print(f"Error during question update: {e}")
                raise RuntimeError(f"Erro ao atualizar pergunta: {e}") from e

    def delete(self, question_id: int):
        with self.__db_connection_handler as database:
            session = database.session
            try:
                q = session.get(Question, question_id)
                if not q:
                    raise RuntimeError("Pergunta não encontrada.")
                session.delete(q)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"Error during question delete: {e}")
                raise RuntimeError(f"Erro ao remover pergunta: {e}") from e
