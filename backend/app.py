from flask import Flask
from controllers import register_blueprints
from models import init_db
from config import configurations, limiter
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from flask_mail import Mail
from flask_caching import Cache  # Importing Flask-Caching

# Initialize extensions
jwt = JWTManager()
mail = Mail()
cache = Cache()  # Initialize cache object


def create_app():
    app = Flask(__name__)

    # Déterminer l'environnement actuel (par défaut : development)
    env = os.getenv("FLASK_ENV", "development")

    # Charger la configuration en fonction de l'environnement
    app.config.from_object(configurations[env])

    with app.app_context():
        init_db()

    CORS(app)
    cache.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
