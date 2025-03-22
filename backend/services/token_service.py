from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from models.token_model import Token
from models import create_session_local
from dtos.token_dto import TokenDTO, token_to_dto
from typing import Optional


def insert_token(token_dto: TokenDTO) -> None:
    """
    Insère un token dans la base de données.
    
    :param token: Le token JWT à stocker.
    """
    session = create_session_local()
    try:
        new_token = Token(token=token_dto.token,
                          data=token_dto.data,
                          salt=token_dto.salt,
                          created_at=token_dto.created_at)
        session.add(new_token)
        session.commit()
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Erreur lors de l'insertion du token : {str(e)}")
    finally:
        session.close()


def delete_token(token: str) -> None:
    """
    Supprime un token de la base de données en fonction de son identifiant.

    :param token: Le token JWT à supprimer.
    """
    session = create_session_local()
    try:
        stored_token = session.query(Token).filter_by(_token=token).first()
        if stored_token:
            session.delete(stored_token)
            session.commit()
        else:
            raise RuntimeError("Token not found")
    except Exception as e:
        session.rollback()
        raise RuntimeError(
            f"Erreur lors de la suppression du token : {str(e)}")
    finally:
        session.close()


def delete_expired_tokens() -> int:
    """
    Supprime les tokens périmés depuis plus d'une heure.
    
    :return: Le nombre de tokens supprimés.
    """
    session = create_session_local()
    try:
        expiration_threshold = datetime.now(timezone.utc) - timedelta(hours=1)
        deleted_count = session.query(Token).filter(
            Token._created_at < expiration_threshold).delete()
        session.commit()
        return deleted_count
    except Exception as e:
        session.rollback()
        raise RuntimeError(
            f"Erreur lors de la suppression des tokens expirés : {str(e)}")
    finally:
        session.close()


def check_token_exists(token: str) -> Optional[TokenDTO]:
    """
    Vérifie si un token existe dans la base de données et retourne un DTO.

    :param token: Le token JWT à vérifier.
    :return: Un objet TokenDTO si le token existe, None sinon.
    """
    session = create_session_local()
    try:
        # Récupérer le token dans la base de données
        stored_token = session.query(Token).filter_by(_token=token).first()

        if stored_token:
            # Si le token existe, convertir en DTO et le retourner
            return token_to_dto(stored_token)
        return None  # Si le token n'existe pas, retourner None

    except Exception as e:
        raise RuntimeError(
            f"Erreur lors de la vérification du token : {str(e)}")
    finally:
        session.close()
