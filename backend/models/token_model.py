from datetime import datetime, timezone
from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime


class Token(Base):
    """
    Represents a token entity in the database.

    Attributes:
        _token (str): The unique token string, serving as the primary key.
        _created_at (datetime): The timestamp when the token was created.
        _data (str): The data associated with the token (e.g., new email or hashed password).
        _salt (str): The salt used for token generation.
    """
    __tablename__ = 'token'

    _token: Mapped[str] = mapped_column("token", String(200), primary_key=True)
    _created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc))  # Utilise maintenant UTC pour le timestamp
    _data: Mapped[str] = mapped_column(
        "data", String(500),
        nullable=True)  # Donnée associée (ex: email, hash)
    _salt: Mapped[str] = mapped_column(
        "salt", String(100),
        nullable=True)  # Salt utilisé pour signer le token

    def __init__(self,
                 token: str,
                 data: str = None,
                 salt: str = None,
                 created_at: datetime = None):
        """
        Initializes a Token instance.

        Args:
            token (str): The token string.
            data (str, optional): Data associated with the token (e.g., email, hashed password).
            salt (str, optional): The salt used for token generation.
            created_at (datetime, optional): The timestamp when the token was created. Defaults to UTC now if None.
        """
        self._token = token
        self._data = data
        self._salt = salt
        # Si `created_at` est passé en argument, l'utiliser. Sinon, utiliser la date UTC actuelle par défaut
        self._created_at = created_at or datetime.now(timezone.utc)
