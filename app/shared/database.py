"""Database infrastructure."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:
    """Database connection manager."""

    def __init__(self, connection_string: str = "sqlite:///DudeWheresMyLambo.db"):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.init_db()

    def init_db(self):
        """Initialize database tables."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new database session."""
        return self.Session()
