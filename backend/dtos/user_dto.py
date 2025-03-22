from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime, date
import re
from typing import Optional
from models.user_model import User


class UserDTO(BaseModel):
    email: EmailStr
    password: Optional[str] = Field(
        None, min_length=8,
        max_length=64)  # Rendre le mot de passe optionnel pour le DTO
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birth_at: Optional[date] = None
    created_at: datetime = None
    login_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permet de convertir depuis un modèle SQLAlchemy

    def to_dict(self) -> dict:
        """Retourne l'objet sous forme de dictionnaire"""
        return self.model_dump(
            exclude={"password"})  # On exclut le password pour la sécurité

    @model_validator(mode='before')
    def validate_password(cls, values):
        """Validation avancée du mot de passe si le champ est présent"""
        password = values.get('password')
        if password:
            if not re.search(r"[A-Z]", password):
                raise ValueError(
                    "Password must contain at least one uppercase letter")
            if not re.search(r"[a-z]", password):
                raise ValueError(
                    "Password must contain at least one lowercase letter")
            if not re.search(r"\d", password):
                raise ValueError("Password must contain at least one digit")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise ValueError(
                    "Password must contain at least one special character")
        return values


# Exemple d'utilisation pour convertir un objet User SQLAlchemy en DTO
def user_to_dto(user: User) -> UserDTO:
    return UserDTO(
        email=user._email,
        password=None,  # Ne pas inclure le mot de passe réel ici
        firstname=user._firstname,
        lastname=user._lastname,
        birth_at=user._birth_at,
        created_at=user._created_at,
        login_at=user._login_at)
