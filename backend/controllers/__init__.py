# from app.controllers.home_page_content_controller import home_page_content_blueprint
from controllers.security_controller import security_blueprint
from controllers.account_controller import account_blueprint


def register_blueprints(app):
    """
    Enregistre les blueprints de l'application Flask.

    Cette fonction enregistre les blueprints `user_blueprint` et `security_blueprint`
    dans l'application Flask, en spécifiant un préfixe d'URL pour `user_blueprint`.

    - `user_blueprint` est enregistré avec le préfixe d'URL `/user`.
    - `security_blueprint` est enregistré sans préfixe d'URL.

    Args:
        app (Flask): L'instance de l'application Flask dans laquelle les blueprints doivent être enregistrés.
    """
    # app.register_blueprint(category_blueprint, url_prefix='/category')
    app.register_blueprint(security_blueprint, url_prefix='/security')
    app.register_blueprint(account_blueprint, url_prefix='/account')
