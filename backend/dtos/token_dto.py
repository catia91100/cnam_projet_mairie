from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional
from models.token_model import Token  # Assure-toi que le modèle Token est bien importé


class TokenDTO(BaseModel):
    token: str  # Le token en tant que string
    created_at: Optional[datetime] = datetime.now(
        timezone.utc)  # Définit la date actuelle en UTC par défaut
    data: str  # Le hash de l'email
    salt: str  # Le salt utilisé

    class Config:
        from_attributes = True  # Permet de convertir depuis un modèle SQLAlchemy

    def to_dict(self) -> dict:
        """Retourne l'objet sous forme de dictionnaire"""
        return self.model_dump()  # Pydantic 2.x utilise model_dump()


# Fonction pour convertir un objet Token SQLAlchemy en DTO
def token_to_dto(token: Token) -> TokenDTO:
    return TokenDTO(
        token=token._token,
        created_at=token._created_at or datetime.now(
            timezone.utc
        ),  # Si 'created_at' est vide, utilise la date actuelle UTC
        data=token.
        _data,  # Le champ 'data' contient les données, comme l'email hashé
        salt=token._salt  # Le salt utilisé dans le modèle
    )
