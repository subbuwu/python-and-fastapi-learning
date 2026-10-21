import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Base - Parent class for all models (maintains metadata)
class Base(DeclarativeBase):
    """Base class for all sqlalchemy models."""
    pass

    # engine manages connection pool to db
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        future=True
    )
    
    # session local is the factory that creates session objects
    
    SessionLocal = sessionmaker(
        bind = engine,
        autoflush=False,
        autocommit=False,
        future=True
    )

