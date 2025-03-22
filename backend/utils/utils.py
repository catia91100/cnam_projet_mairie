import string, secrets, os, jwt, hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from flask import current_app
from jinja2 import Template
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import create_access_token
from dtos.token_dto import TokenDTO  # Assure-toi que le DTO TokenDTO est bien importé


def generate_psw(length: int = 20) -> str:
    """Génère un mot de passe sécurisé respectant les critères de validation."""

    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # Assurer la présence d'au moins un caractère de chaque type
    mandatory_chars = [
        secrets.choice(string.ascii_uppercase),  # 1 majuscule
        secrets.choice(string.ascii_lowercase),  # 1 minuscule
        secrets.choice(string.digits),  # 1 chiffre
        secrets.choice(string.punctuation)  # 1 caractère spécial
    ]

    # Compléter avec des caractères aléatoires jusqu'à la longueur demandée
    remaining_chars = [
        secrets.choice(string.ascii_letters + string.digits +
                       string.punctuation)
        for _ in range(length - len(mandatory_chars))
    ]

    # Mélanger tous les caractères pour éviter un motif prévisible
    password_list = mandatory_chars + remaining_chars
    secrets.SystemRandom().shuffle(password_list)

    return ''.join(password_list)


def hash_password(password: str) -> str:
    """Hache un mot de passe en utilisant Werkzeug.
    
    Args:
        password (str): Le mot de passe en clair.

    Returns:
        str: Le mot de passe haché.
    """
    return generate_password_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si un mot de passe correspond à son hachage.
    
    Args:
        plain_password (str): Le mot de passe en clair.
        hashed_password (str): Le mot de passe haché.

    Returns:
        bool: True si le mot de passe correspond, False sinon.
    """
    return check_password_hash(hashed_password, plain_password)


def send_email(subject: str,
               recipients: list,
               template: str,
               context: dict,
               sender: str = None):
    """
    Envoie un email avec Flask-Mail en utilisant un template Jinja2 et un dictionnaire de variables.
    
    :param subject: Sujet de l'email
    :param recipients: Liste des destinataires (email(s))
    :param template: Nom du template HTML ou texte
    :param context: Dictionnaire des variables pour le template
    :param sender: (optionnel) Expéditeur de l'email (par défaut, utilise la config)
    """
    if sender is None:
        sender = current_app.config[
            'MAIL_DEFAULT_SENDER']  # Utilisation de la valeur par défaut si non précisé

    # Chargement du template
    with open(os.path.join(current_app.root_path, 'templates', template),
              'r') as file:
        template_content = file.read()

    # Utilisation de Jinja2 pour remplir le template avec les variables contextuelles
    template_obj = Template(template_content)
    body = template_obj.render(context)

    # Création du message
    msg = Message(subject=subject,
                  recipients=recipients,
                  sender=sender,
                  html=body)

    # Envoi du message
    try:
        current_app.extensions['mail'].send(
            msg)  # Utilisation de l'instance mail initialisée dans app.py
        return True  # Indique que l'email a été envoyé avec succès
    except Exception as e:
        # En cas d'erreur lors de l'envoi
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")
        return False


# def generate_token(email: str, expiration_hours: int = 1):
#     from dtos.token_dto import TokenDTO
#     expiration = datetime.now(timezone.utc) + timedelta(hours=expiration_hours)

#     # Générer le token JWT
#     token = jwt.encode(
#         {
#             'email': email,
#             'exp': expiration
#         },
#         current_app.
#         config['JWT_SECRET_KEY'],  # Utilise ta propre clé secrète ici
#         algorithm='HS256')

#     # Retourner un DTO avec le token et l'expiration
#     return TokenDTO(token=token, expiration=expiration)

# def generate_token(email: str, expiration_hours: int = 1, claims: dict = None):
#     """Generate a JWT token for the user using flask_jwt_extended, with optional custom claims."""
#     try:
#         # Générer le token en utilisant la méthode de flask_jwt_extended
#         return create_access_token(
#             identity=email,
#             expires_delta=timedelta(hours=expiration_hours),
#             additional_claims=claims if claims else {})

#     except Exception as e:
#         raise Exception(f"Error generating token: {str(e)}")


def generate_token(email: str,
                   expiration_hours: int = 1,
                   claims: dict = None,
                   salt: str = "") -> str:
    """Generate a JWT token with a salt modifying the signing secret."""
    try:
        # Générer une clé secrète modifiée avec le SALT
        original_secret_key = current_app.config['JWT_SECRET_KEY']
        if salt:
            # Ajouter le salt au secret de base
            current_app.config['JWT_SECRET_KEY'] = hashlib.sha256(
                (original_secret_key + salt).encode()).hexdigest()

        # Générer le token avec la clé secrète modifiée
        token = create_access_token(
            identity=email,
            expires_delta=timedelta(hours=expiration_hours),
            additional_claims=claims if claims else {})

        # Rétablir la clé secrète d'origine après la génération du token
        current_app.config['JWT_SECRET_KEY'] = original_secret_key

        return token  # Retourne simplement le token sous forme de string

    except Exception as e:
        raise Exception(f"Error generating token: {str(e)}")


# def decode_token_custom(token: str, salt: str = ""):
#     """Decode a JWT token using a modified secret key with a salt."""
#     try:
#         # Récupérer la clé secrète originale
#         secret_key = current_app.config['JWT_SECRET_KEY']

#         # Appliquer le même SALT que lors de la génération
#         if salt:
#             secret_key = hashlib.sha256(
#                 (secret_key + salt).encode()).hexdigest()

#         # Décoder le token
#         decoded_data = jwt.decode(token, secret_key, algorithms=["HS256"])

#         return decoded_data  # Retourne le contenu du token

#     except jwt.ExpiredSignatureError:
#         return {"error": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"error": "Invalid token"}
#     except Exception as e:
#         return {"error": f"An unexpected error occurred: {str(e)}"}


def decode_token_custom(token: str, salt: str):
    """Décoder un token JWT avec un salt utilisé pour générer la clé secrète."""
    try:
        # Récupérer la clé secrète d'origine
        original_secret_key = current_app.config['JWT_SECRET_KEY']

        # Modifie la clé secrète avec le SALT fourni
        if salt:
            current_app.config['JWT_SECRET_KEY'] = hashlib.sha256(
                (original_secret_key + salt).encode()).hexdigest()

        # Décoder le token avec la clé secrète modifiée
        decoded_token = jwt.decode(token,
                                   current_app.config['JWT_SECRET_KEY'],
                                   algorithms=['HS256'])

        # Rétablir la clé secrète d'origine après le décodage
        current_app.config['JWT_SECRET_KEY'] = original_secret_key

        # Retourner le contenu du token décodé (par exemple, l'email)
        return decoded_token

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    except Exception as e:
        raise Exception(f"Error decoding token: {str(e)}")
