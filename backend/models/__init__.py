from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from flask import current_app


# Base model for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


def get_engine():
    """
    Returns the database engine based on the Flask app's configuration.
    """
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'],
                           echo=True)
    return engine


def init_db():
    """
    Initializes the database and creates all tables based on SQLAlchemy models.
    """
    engine = get_engine()  # Retrieve the database engine

    # Import all models here, make sure they are registered before creating the tables
    from models.token_model import Token
    from models.role_model import Role
    from models.user_model import User
    # If other models exist, un-comment their import lines:
    # from models.category_model import Category
    # from models.event_model import Event
    # etc.

    Base.metadata.create_all(engine)  # Create all tables for the models


def create_session_local():
    # Crée la session à partir de sessionmaker, mais retourne directement la session
    SessionLocal = sessionmaker(autocommit=False,
                                autoflush=False,
                                bind=get_engine())
    return SessionLocal()
