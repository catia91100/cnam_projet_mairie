from datetime import datetime, timezone, date
from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime
from typing import Optional

aware_datetime = datetime.now(timezone.utc)


class User(Base):

    __tablename__ = 'user'

    _email: Mapped[str] = mapped_column("email", String(50), primary_key=True)
    _password: Mapped[str] = mapped_column("password", String(50))
    _firstname: Mapped[Optional[str]] = mapped_column("firstname")
    _lastname: Mapped[Optional[str]] = mapped_column("lastname")
    _birth_at: Mapped[Optional[date]] = mapped_column("birth_at")
    _created_at: Mapped[datetime] = mapped_column("created_at",
                                                  DateTime(timezone=True),
                                                  default=aware_datetime)
    _login_at: Mapped[Optional[datetime]] = mapped_column("login_at")

    def __init__(self,
                 email: str,
                 password: str = None,
                 firstname: str = None,
                 lastname: str = None,
                 birth_at: datetime = None,
                 login_at: datetime = None):
        """
        Constructeur de la classe User.
        
        :param email: L'email de l'utilisateur (obligatoire).
        :param password: Le mot de passe haché de l'utilisateur (optionnel).
        :param firstname: Le prénom de l'utilisateur (optionnel).
        :param lastname: Le nom de famille de l'utilisateur (optionnel).
        :param birth_at: La date de naissance de l'utilisateur (optionnel).
        :param login_at: La date de la dernière connexion de l'utilisateur (optionnel).
        """
        self._email = email
        self._password = password
        self._firstname = firstname
        self._lastname = lastname
        self._birth_at = birth_at
        self._login_at = login_at

    def __repr__(self):

        return (
            f'<User(email={self.get_email()},role={self.get_role()}, firstname={self.get_firstname()}, '
            f'lastname={self.get_lastname()}, birth_at={self.get_birth_at()}, '
            f'created_at={self.get_created_at()}, login_at={self.get_login_at()}, password={self.get_password()})>'
        )
