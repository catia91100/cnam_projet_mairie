from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import get_user_by_email, update_user  # Assuming this function is in services/user_service.py
from dtos.user_dto import user_to_dto  # Assuming this function is in dtos/user_dto.py
from services.token_service import check_token_exists, delete_token, delete_expired_tokens, insert_token
from utils.utils import generate_token, send_email
from datetime import datetime

# Création du blueprint 'account'
account_blueprint = Blueprint('account', __name__)


class Account:

    @staticmethod
    @account_blueprint.route('', methods=['GET'])
    @jwt_required()  # Protect the route with JWT authentication
    def index():
        try:
            # Récupérer l'email de l'utilisateur depuis le JWT
            email = get_jwt_identity()

            # Utiliser l'email pour récupérer les données de l'utilisateur
            user = get_user_by_email(email)

            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Convertir les données de l'utilisateur en DTO et les retourner en JSON
            user_dto = user_to_dto(user)
            return jsonify(user_dto.to_dict()), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    # @staticmethod
    # @account_blueprint.route('/update', methods=['PUT'])
    # @jwt_required()
    # def update_account():
    #     try:
    #         # Récupérer l'email de l'utilisateur connecté depuis le JWT
    #         email = get_jwt_identity()

    #         # Récupérer l'utilisateur depuis la base de données avec l'email
    #         user = get_user_by_email(email)
    #         if not user:
    #             return jsonify({'error': 'User not found'}), 404

    #         # Récupérer les données envoyées dans la requête
    #         data = request.json if request.json else {}

    #         # Fonction pour parser une date correctement
    #         def parse_date(value):
    #             if isinstance(value, str):
    #                 try:
    #                     return datetime.strptime(
    #                         value, "%a, %d %b %Y %H:%M:%S GMT").date()
    #                 except ValueError:
    #                     return None  # Si la date est invalide
    #             return value  # Si déjà une date, renvoyer telle quelle

    #         # Compléter les données manquantes avec celles en base
    #         updated_data = {
    #             "email": user._email,  # Correction : Ajout de l'email
    #             "firstname": data.get("firstname", user._firstname),
    #             "lastname": data.get("lastname", user._lastname),
    #             "birth_at": parse_date(data.get("birth_at", user._birth_at)),
    #             "login_at": parse_date(data.get("login_at", user._login_at))
    #         }

    #         # Vérifier si un nouvel email est fourni
    #         new_email = data.get("email")
    #         token = None

    #         if new_email and new_email != user._email:
    #             try:
    #                 valid_email = EmailStr(new_email)

    #                 # Vérifier si l'email existe déjà
    #                 if get_user_by_email(new_email):
    #                     return jsonify({'error': 'Email already taken'}), 400

    #                 # Générer un token pour la validation
    #                 claims = {"new_email": new_email}
    #                 token = generate_token(email=user._email,
    #                                        expiration_hours=1,
    #                                        claims=claims)

    #                 # Persister le token
    #                 insert_token(token)

    #             except ValidationError:
    #                 return jsonify({'error': 'Invalid email format'}), 400

    #         # Vérifier si des données ont changé
    #         if updated_data or token:
    #             user_dto = UserDTO(**updated_data)
    #             update_user(email, user_dto)  # Mise à jour en base

    #             if new_email:
    #                 validation_url = f"{current_app.config['BASE_URL']}/account/update-email?token={token}"
    #                 context = {
    #                     "user_email": updated_data["firstname"],
    #                     "validation_url": validation_url,
    #                     "current_year": datetime.now().year
    #                 }
    #                 send_email("Please validate your new email", [new_email],
    #                            "mail/email_new.html", context)

    #             delete_expired_tokens()

    #             updated_user = get_user_by_email(email)
    #             response = {
    #                 'message': 'Account updated successfully',
    #                 'user': user_to_dto(updated_user).to_dict()
    #             }

    #             if new_email:
    #                 response['token'] = token

    #             return jsonify(response), 200

    #         return jsonify({'message': 'No changes detected'}), 400

    #     except ValidationError as e:
    #         return jsonify({
    #             'error': 'Invalid data',
    #             'details': e.errors()
    #         }), 400

    #     except Exception as e:
    #         return jsonify({
    #             'error': 'An unexpected error occurred',
    #             'details': str(e)
    #         }), 500

    @staticmethod
    @account_blueprint.route('/update-email', methods=['GET'])
    def update_email_from_token():
        try:
            # Récupérer le token depuis l'URL
            token = request.args.get('token')
            if not token:
                return jsonify({'error': 'Token is missing'}), 400

            # Vérifier si le token existe dans la table des tokens
            if not check_token_exists(token):
                return jsonify({'error': 'Invalid or already used token'}), 400

            # Supprimer le token après utilisation pour éviter toute réutilisation
            delete_token(token)

            # Nettoyer les tokens périmés de la table
            delete_expired_tokens()

            # Décoder le token pour récupérer l'email de l'utilisateur et le new_email
            try:
                decoded_token = current_app.extensions['jwt_manager'].decode(
                    token,
                    current_app.config['JWT_SECRET_KEY'],
                    algorithms=['HS256'])
                email = decoded_token.get(
                    'sub'
                )  # Récupère l'email actuel de l'utilisateur dans le token
                new_email = decoded_token.get(
                    'new_email')  # Récupère le nouvel email dans les claims
                if not new_email:
                    return jsonify({'error':
                                    'New email is missing in token'}), 400
            except current_app.extensions['jwt_manager'].ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 400
            except current_app.extensions['jwt_manager'].InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 400

            # Récupérer l'utilisateur actuel depuis la base de données
            user = get_user_by_email(email)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Vérifier si le nouvel email existe déjà en base
            existing_user = get_user_by_email(new_email)
            if existing_user:
                return jsonify({'error':
                                'The new email is already in use'}), 400

            # Mettre à jour l'email de l'utilisateur
            user.email = new_email
            updated_user = update_user(
                email, user)  # Met à jour l'utilisateur en base de données

            # Retourner la réponse JSON
            return jsonify({
                'message': 'Email updated successfully',
                'user': updated_user.to_dict()
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @account_blueprint.route('/update', methods=['PUT'])
    @jwt_required()
    def update_account():
        try:
            # Récupérer l'email de l'utilisateur connecté depuis le JWT
            email = get_jwt_identity()

            # Récupérer l'utilisateur en base de données
            user = get_user_by_email(email)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Récupérer les données envoyées dans la requête
            data = request.get_json()
            if not data:
                return jsonify({'error':
                                'Invalid request, JSON required'}), 400

            # Vérifier si un email a été fourni dans les données postées
            new_email = data.get('email')
            token = None  # Initialisation du token

            if new_email and new_email != user._email:
                # Vérifier si l'email existe déjà en base
                existing_user = get_user_by_email(new_email)
                if existing_user:
                    return jsonify({'error': 'Email already taken'}), 400

                # Générer un token JWT pour la validation du nouvel email
                claims = {"new_email": new_email}
                token = generate_token(email=user._email,
                                       expiration_hours=1,
                                       claims=claims)
                validation_url = f"{current_app.config['BASE_URL']}/account/update-email?token={token}"
                context = {
                    "user_email": updated_data["firstname"],
                    "validation_url": validation_url,
                    "current_year": datetime.now().year
                }
                send_email("Please validate your new email", [new_email],
                           "mail/email_new.html", context)

            return jsonify({
                'message': 'User and data retrieved successfully',
                'user': user_to_dto(user).to_dict(),
                'posted_data': data,
                'email_verification_token':
                token  # Retourner le token si généré
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500
