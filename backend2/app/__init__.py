from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt, jwt

from .routes.user import user_bp
from .routes.auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)   
    # Enregistrement des Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # Initialisation de la base de données
    return app