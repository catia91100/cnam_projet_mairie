from sqlalchemy.orm import Session
from models.user_model import User
from dtos.user_dto import UserDTO
from utils.utils import hash_password  # Supposons que tu as une fonction pour hacher le mot de passe
from models import create_session_local  # Ajout de create_session_local
from utils.utils import verify_password
from datetime import datetime


def insert_user(user_dto: UserDTO) -> User:
    """Insère un utilisateur dans la base de données à partir d'un DTO.
    
    Args:
        user_dto (UserDTO): L'objet DTO contenant les informations de l'utilisateur.

    Returns:
        User: L'objet utilisateur inséré en base de données.
    """
    session = create_session_local()  # Créer une session locale
    try:
        new_user = User(
            email=user_dto.email,
            password=user_dto.password,  # Hacher le mot de passe
            firstname=user_dto.firstname,
            lastname=user_dto.lastname,
            birth_at=user_dto.birth_at,
            login_at=user_dto.login_at)

        session.add(new_user)
        session.commit()
        session.refresh(
            new_user)  # Rafraîchir pour récupérer les nouvelles valeurs
        return new_user
    except Exception as e:
        session.rollback()
        raise ValueError(
            f"Erreur lors de l'insertion de l'utilisateur : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def verify_login(email: str, password: str) -> bool:
    """Vérifie si les informations de connexion (email et mot de passe) sont valides.

    Args:
        email (str): L'email de l'utilisateur à vérifier.
        password (str): Le mot de passe fourni par l'utilisateur.

    Returns:
        bool: True si l'email et le mot de passe sont valides, False sinon.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'utilisateur par email
        user = session.query(User).filter_by(_email=email).first()

        if not user:
            # Si l'utilisateur n'existe pas, retourner False
            return False

        # Vérification du mot de passe
        if verify_password(
                password, user._password
        ):  # Utilisez la fonction check_password pour vérifier les mots de passe
            return True
        else:
            return False
    except Exception as e:
        # Si une erreur se produit, renvoyer False
        print(f"Erreur lors de la vérification du login : {str(e)}")
        return False
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def get_user_by_email(email: str) -> User:
    """Récupère un utilisateur de la base de données en fonction de son email.
    
    Args:
        email (str): L'email de l'utilisateur à récupérer.
    
    Returns:
        User: L'utilisateur trouvé ou None si l'utilisateur n'existe pas.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'utilisateur par email
        user = session.query(User).filter_by(_email=email).first()

        return user  # Retourne l'utilisateur trouvé, ou None si pas trouvé.

    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")
        return None

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_user(email: str, user_dto: UserDTO) -> User:
    """Met à jour les informations d'un utilisateur à partir d'un DTO.

    Args:
        email (str): L'email de l'utilisateur à mettre à jour.
        user_dto (UserDTO): L'objet DTO contenant les nouvelles informations de l'utilisateur.

    Returns:
        User: L'objet utilisateur mis à jour.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'utilisateur par email
        user = session.query(User).filter_by(_email=email).first()

        if not user:
            raise ValueError(f"Utilisateur avec l'email {email} non trouvé.")

        # Mise à jour des champs de l'utilisateur
        if user_dto.firstname:
            user._firstname = user_dto.firstname
        if user_dto.lastname:
            user._lastname = user_dto.lastname
        if user_dto.birth_at:
            user._birth_at = user_dto.birth_at
        if user_dto.login_at:
            user._login_at = user_dto.login_at

        # Si un nouveau mot de passe est fourni, on le hache et on met à jour
        if user_dto.password:
            user._password = hash_password(
                user_dto.password)  # Hachage du mot de passe

        # Sauvegarde des modifications
        session.commit()
        session.refresh(
            user)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return user  # Retourner l'utilisateur mis à jour

    except Exception as e:
        session.rollback()
        raise ValueError(
            f"Erreur lors de la mise à jour de l'utilisateur : {str(e)}")

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_login_at(email: str) -> User:
    """Met à jour le champ login_at de l'utilisateur avec l'horodatage actuel.

    Args:
        email (str): L'email de l'utilisateur dont on veut mettre à jour le login_at.

    Returns:
        User: L'utilisateur mis à jour.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Récupérer l'utilisateur par son email
        user = session.query(User).filter_by(_email=email).first()

        if not user:
            raise ValueError(f"Utilisateur avec l'email {email} non trouvé.")

        # Mettre à jour le champ login_at avec la date et l'heure actuelles
        user._login_at = datetime.utcnow()

        # Sauvegarder les modifications
        session.commit()
        session.refresh(
            user)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return user  # Retourner l'utilisateur mis à jour

    except Exception as e:
        session.rollback()
        raise ValueError(
            f"Erreur lors de la mise à jour du login_at : {str(e)}")

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_user_email(old_email: str, new_user_dto: UserDTO) -> User:
    """Met à jour l'email d'un utilisateur.

    Args:
        old_email (str): L'email actuel de l'utilisateur.
        new_email (str): Le nouvel email de l'utilisateur.

    Returns:
        User: L'objet utilisateur mis à jour avec le nouvel email.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'utilisateur par l'ancien email
        user = session.query(User).filter_by(_email=old_email).first()

        if not user:
            raise ValueError(
                f"Utilisateur avec l'email {old_email} non trouvé.")

        # Vérifier si le nouvel email est déjà pris
        if session.query(User).filter_by(_email=new_user_dto.email).first():
            raise ValueError(
                f"L'email {new_user_dto.email} est déjà associé à un autre utilisateur."
            )

        # Mise à jour de l'email
        user._email = new_user_dto.email

        # Sauvegarde des modifications
        session.commit()
        session.refresh(
            user)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return user  # Retourner l'utilisateur mis à jour avec le nouvel email

    except Exception as e:
        session.rollback()
        raise ValueError(
            f"Erreur lors de la mise à jour de l'email de l'utilisateur : {str(e)}"
        )

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin
