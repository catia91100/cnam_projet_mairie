from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


class Config:
    """
    Configuration de base pour l'application.

    Cette classe définit les paramètres de configuration par défaut pour l'application,
    y compris l'URI de la base de données, le mode de test et la clé secrète pour JWT.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///bd/exemple.db"
    TESTING = False
    JWT_SECRET_KEY = 'super-secret'

    BASE_URL = 'http://localhost:5000'

    # Configuration du serveur mail (développement par défaut)
    MAIL_SERVER: str = os.getenv('MAIL_SERVER', "127.168.1.1")
    MAIL_PORT: int = os.getenv('MAIL_PORT', 1025)
    MAIL_USE_TLS: bool = os.getenv('MAIL_USE_TLS', False)
    MAIL_USE_SSL: bool = os.getenv('MAIL_USE_SSL', False)
    MAIL_USERNAME: str | None = os.getenv('MAIL_USERNAME', None)
    MAIL_PASSWORD: str | None = os.getenv('MAIL_PASSWORD', None)
    MAIL_DEFAULT_SENDER: str = os.getenv('MAIL_DEFAULT_SENDER',
                                         "mairie@gmail.com")
    MAIL_MAX_EMAILS: int | None = None
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


# class ProductionConfig(Config):
#     """
#     Configuration spécifique à la production.

#     Active un serveur mail sécurisé et redéfinit l'URL de base.
#     """
#     # BASE_URL = "https://mon-site.com"

#     # Configuration du serveur SMTP en production
#     MAIL_SERVER = "MAIL_SERVER"
#     MAIL_PORT = 000
#     MAIL_USE_TLS = True
#     MAIL_USE_SSL = False  # On utilise TLS et non SSL
#     MAIL_USERNAME = "MAIL_USERNAME"
#     MAIL_PASSWORD = "MAIL_PASSWORD"
#     MAIL_DEFAULT_SENDER = "MAIL_DEFAULT_SENDER"

# Dictionnaire pour sélectionner la bonne configuration en fonction de l'environnement
configurations = {
    "development": Config,
    "testing": TestConfig,
    "production": Config
}
