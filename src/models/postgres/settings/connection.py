from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .configs import database_configs


class DBConnectionHandler:
    """
    Connect DB
    """

    def __init__(self) -> None:
        self.__connection_string = f"{database_configs.DATABASE_URL}"
        self.__engine = None
        self.session = None
        self.Session = None

    def connect_to_db(self) -> None:
        if self.__engine is None:
            self.__engine = create_engine(self.__connection_string)
            self.Session = sessionmaker(bind=self.__engine)
            print("Engine criado:", self.__engine)

    def get_engine(self):
        self.connect_to_db()
        return self.__engine

    def __enter__(self):
        self.connect_to_db()
        if self.Session is None:
            self.Session = sessionmaker(bind=self.__engine)
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
            self.session = None


db_connection_handler = DBConnectionHandler()
