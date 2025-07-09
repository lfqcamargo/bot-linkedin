from abc import ABC, abstractmethod
from typing import Optional, List
import datetime
from src.models.postgres.entities.user import User

class UsersRepositoryInterface(ABC):

    @abstractmethod
    def create(
        self,
        name: str,
        email: str,
        password: str,
        birthday_date: datetime.date,
        curriculum: bytes,
        phone: str
    ) -> User:
        pass

    @abstractmethod
    def update(
        self,
        user_id: int,
        name: str,
        email: str,
        password: str,
        birthday_date: datetime.date,
        curriculum: bytes,
        country_code: str,
        phone: str
    ) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def fetch_all(self) -> List[User]:
        pass
