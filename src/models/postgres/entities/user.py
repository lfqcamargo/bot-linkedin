from sqlalchemy.types import LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from src.models.postgres.settings.base import Base


class User(Base):
    """
    User
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    birthday_date: Mapped[datetime.date] = mapped_column()
    curriculum: Mapped[bytes] = mapped_column(LargeBinary)
    phone: Mapped[str] = mapped_column(String(20))
