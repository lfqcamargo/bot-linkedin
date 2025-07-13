from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum as SQLEnum
from src.models.postgres.settings.base import Base
from pgvector.sqlalchemy import Vector
from datetime import datetime

from enum import Enum


class QuestionTypes(Enum):
    """
    Enumeration representing the possible HTML input types for a question.

    Attributes:
        TEXT (str): Represents a text input.
        NUMBER (str): Represents a number input.
        DATE (str): Represents a date input.
        EMAIL (str): Represents an email input.
        PASSWORD (str): Represents a password input.
        CHECKBOX (str): Represents a checkbox input.
        RADIO (str): Represents a radio button input.
        SELECT (str): Represents a select (dropdown) input.
        TEXTAREA (str): Represents a multiline text area input.
    """

    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    EMAIL = "email"
    PASSWORD = "password"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    SELECT = "select"
    TEXTAREA = "textarea"
    SELECT_ONE = "select-one"


class Question(Base):
    """
    Question.
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    question_type = Column(SQLEnum(QuestionTypes), nullable=False)
    question = Column(String(255), nullable=False)
    embeddings = Column(Vector(768))
    response = Column(String, nullable=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
