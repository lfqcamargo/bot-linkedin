from src.models.postgres.entities.user import User
from src.models.postgres.interfaces.users_repository_interface import UsersRepositoryInterface
from sqlalchemy.orm import Session
from typing import cast, List, Optional
import datetime

class UsersRepository(UsersRepositoryInterface):
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def create(
        self,
        name: str,
        email: str,
        password: str,
        birthday_date: datetime.date,
        curriculum: bytes,
        phone: str
    ) -> User:
        with self.__db_connection as database:
            session: Session = cast(Session, database.session)
            user = User(
                name=name,
                email=email,
                password=password,
                birthday_date=birthday_date,
                curriculum=curriculum,
                phone=phone
            )
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except Exception as e:
                session.rollback()
                print(f"Error during user creation: {e}")
                raise RuntimeError(f"Erro ao criar usuário: {e}") from e

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
    ) -> bool:
        with self.__db_connection as database:
            session: Session = cast(Session, database.session)
            db_user = session.query(User).filter(User.id == user_id).first()
            if not db_user:
                return False

            db_user.name = name
            db_user.email = email
            db_user.password = password
            db_user.birthday_date = birthday_date
            db_user.curriculum = curriculum
            db_user.country_code = country_code
            db_user.phone = phone

            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"Error during user update: {e}")
                return False

    def delete(self, user_id: int) -> bool:
        with self.__db_connection as database:
            session: Session = cast(Session, database.session)
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            try:
                session.delete(user)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"Error during user deletion: {e}")
                return False

    def find_by_email(self, email: str) -> Optional[User]:
        with self.__db_connection as database:
            session: Session = cast(Session, database.session)
            return session.query(User).filter(User.email == email).first()

    def fetch_all(self) -> List[User]:
        with self.__db_connection as database:
            session: Session = cast(Session, database.session)
            return list(session.query(User).all())
