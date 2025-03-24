from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv  # Ajout de python-dotenv pour charger les variables d'environnement
from typing import Optional

# Charger les variables d'environnement depuis un fichier .env
load_dotenv(
    '.env'
)  # Charge les variables d'environnement spécifiques au dev (si tu utilises un fichier .env.dev)

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # Assure-toi que le stockage en mémoire est utilisé
)


class Config:
    """
    Configuration de base pour l'application.
    
    Cette classe définit les paramètres de configuration par défaut pour l'application,
    y compris l'URI de la base de données, le mode de test et la clé secrète pour JWT.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/exemple.db"
    TESTING = False
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY',
        'super-secret')  # Utilisation de la variable d'environnement

    BASE_URL: str = os.getenv('NEXT_PUBLIC_API_URL', 'http://localhost:5000')

    # Configuration du serveur mail (développement par défaut)
    MAIL_SERVER: str = os.getenv('MAIL_SERVER', "127.0.0.1")
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', 1025))
    MAIL_USE_TLS: bool = os.getenv('MAIL_USE_TLS',
                                   'False').lower() in ('true', '1', 'yes')
    MAIL_USE_SSL: bool = os.getenv('MAIL_USE_SSL',
                                   'False').lower() in ('true', '1', 'yes')
    MAIL_USERNAME: Optional[str] = os.getenv('MAIL_USERNAME', None)
    MAIL_PASSWORD: Optional[str] = os.getenv('MAIL_PASSWORD', None)
    MAIL_DEFAULT_SENDER: str = os.getenv('MAIL_DEFAULT_SENDER',
                                         "mairie@gmail.com")
    MAIL_MAX_EMAILS: Optional[int] = None
    MAIL_ASCII_ATTACHMENTS: bool = False

    UPLOAD_FOLDER = './static/img'

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300


class TestConfig(Config):
    """
    Configuration spécifique aux tests.

    Redéfinit certains paramètres pour les tests, notamment l'URI de la base de données.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class ProductionConfig(Config):
    """
    Configuration spécifique à la production.

    Active un serveur mail sécurisé et redéfinit l'URL de base.
    """
    # BASE_URL = "https://mon-site.com"

    # Configuration du serveur SMTP en production
    MAIL_SERVER = os.getenv("MAIL_SERVER", "MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))  # Valeur par défaut du port
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS",
                             "True").lower() in ('true', '1', 'yes')
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL",
                             "False").lower() in ('true', '1', 'yes')
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER",
                                    "MAIL_DEFAULT_SENDER")


# Dictionnaire pour sélectionner la bonne configuration en fonction de l'environnement
configurations = {
    "development": Config,
    "testing": TestConfig,
    "production": ProductionConfig  # Utiliser une configuration spécifique
}
