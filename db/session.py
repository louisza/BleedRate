"""Database session management"""
from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency for database sessions"""
    with Session(engine) as session:
        yield session
