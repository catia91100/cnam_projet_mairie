from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime, date
import re
from typing import Optional
from models.user_model import User


class UserDTO(BaseModel):
    email: EmailStr
    password: Optional[str] = Field(None,
                                    min_length=8,
                                    max_length=64,
                                    strict=True)
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birth_at: Optional[date] = None
    created_at: Optional[datetime] = None
    login_at: Optional[datetime] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True  # Permet de convertir depuis un modèle SQLAlchemy

    def to_dict(self) -> dict:
        """Retourne l'objet sous forme de dictionnaire"""
        return self.model_dump()  # Exclut le mot de passe
        return self.model_dump(exclude={"password"})  # Exclut le mot de passe

    @model_validator(mode='after')
    def validate_password(cls, instance):
        """Validation avancée du mot de passe après l'instanciation"""
        password = instance.password
        print(password, 'kdsofllllllllllllllllllllu')
        if password:  # Vérifie si le mot de passe est défini
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

        return instance  # Retourne l'instance validée

    @model_validator(mode='before')
    def validate_birth_at(cls, values):
        # """Validation avancée des champs (password & birth_at)"""
        # # Validation du mot de passe (inchangée)
        # password = values.get('password')
        # if password:
        #     if not re.search(r"[A-Z]", password):
        #         raise ValueError(
        #             "Password must contain at least one uppercase letter")
        #     if not re.search(r"[a-z]", password):
        #         raise ValueError(
        #             "Password must contain at least one lowercase letter")
        #     if not re.search(r"\d", password):
        #         raise ValueError("Password must contain at least one digit")
        #     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        #         raise ValueError(
        #             "Password must contain at least one special character")

        # Conversion de `birth_at` si nécessaire
        birth_at = values.get('birth_at')
        if isinstance(birth_at, str):
            try:
                # Essaye de parser la date de naissance
                birth_at = datetime.strptime(birth_at, "%Y-%m-%d").date()
                values["birth_at"] = birth_at
                print(f"Converted birth_at: {birth_at}")
            except ValueError:
                raise ValueError("Invalid date format for birth_at")

        # Conversion des autres dates (created_at, login_at)
        for date_field in ['created_at', 'login_at']:
            date_value = values.get(date_field)
            if isinstance(date_value, str):
                try:
                    # Essaye de parser les autres dates
                    date_value = datetime.strptime(
                        date_value, "%a, %d %b %Y %H:%M:%S GMT")
                    values[date_field] = date_value
                    print(f"Converted {date_field}: {date_value}")
                except ValueError:
                    raise ValueError(f"Invalid date format for {date_field}")

        return values

    @model_validator(mode='after')
    def check_dates(cls, instance):
        """Vérifie que `birth_at`, `created_at`, `login_at` sont bien des dates"""
        # Vérifier que toutes les dates sont bien au bon format
        for date_field in ['birth_at', 'created_at', 'login_at']:
            date_value = getattr(instance, date_field)
            if date_value is not None and not isinstance(
                    date_value, (date, datetime)):
                raise ValueError(
                    f"{date_field} must be a valid date or datetime, but got {type(date_value)}"
                )

        return instance


# Exemple d'utilisation pour convertir un objet User SQLAlchemy en DTO
def user_to_dto(user: User) -> UserDTO:
    return UserDTO(
        email=user._email,
        password=None
        or user._password,  # Ne pas inclure le mot de passe réel ici
        firstname=user._firstname,
        lastname=user._lastname,
        birth_at=user._birth_at,
        created_at=user._created_at,
        login_at=user._login_at,
        role=user._role)
