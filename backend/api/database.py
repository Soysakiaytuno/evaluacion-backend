import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

Base = declarative_base()

class PostgresSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresSingleton, cls).__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL)
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
        return cls._instance

    def get_session(self):
        return self.SessionLocal()

postgres_db = PostgresSingleton()

def get_db():
    db = postgres_db.get_session()
    try:
        yield db
    finally:
        db.close()