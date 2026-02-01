"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Create base class for declarative models
Base = declarative_base()

# Database URL (SQLite by default)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///emploi_du_temps.db')

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    poolclass=StaticPool if DATABASE_URL.startswith("sqlite") else None,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """
    Get a database session.
    
    Usage:
        with get_session() as session:
            # Use session here
            pass
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Initialize the database by creating all tables."""
    # Import all models to ensure they're registered
    from database import models
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("[OK] Database initialized successfully!")


def drop_all():
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("[Warning] All tables dropped!")
