
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Engine manages database connections and the connection pool
engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# SessionLocal creates database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
