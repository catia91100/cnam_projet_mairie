from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import get_user_by_email, update_user, update_user_email  # Assuming this function is in services/user_service.py
from dtos.user_dto import user_to_dto  # Assuming this function is in dtos/user_dto.py
from services.token_service import check_token_exists, delete_token, delete_expired_tokens, insert_token
from utils.utils import generate_token, send_email, decode_token_custom
from datetime import datetime
import hashlib, uuid
from dtos.user_dto import UserDTO
from dtos.token_dto import TokenDTO
from models.user_model import User

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

    @staticmethod
    @account_blueprint.route('/update-email', methods=['GET'])
    def update_email_from_token():
        try:
            # Récupérer le token depuis l'URL
            token = request.args.get('token')
            if not token:
                return jsonify({'error': 'Token is missing'}), 400

            # Vérifier si le token existe dans la table des tokens
            token_dto: TokenDTO = check_token_exists(token)
            if not token_dto:
                return jsonify({'error': 'Invalid or already used token'}), 400

            # Supprimer le token après utilisation pour éviter toute réutilisation
            # delete_token(token)

            # Nettoyer les tokens périmés de la table
            delete_expired_tokens()

            # print(f"yzteeeeeeeeeee {token}")

            # Décoder le token pour récupérer l'email de l'utilisateur et le new_email

            try:
                decoded_token = decode_token_custom(token, token_dto.salt)
                email = decoded_token.get('sub')
                new_email = decoded_token.get('new_email')
                if not new_email:
                    return jsonify({'error': 'Invalid token'}), 400
                # Vérifier la correspondance avec l'email hashé stocké dans le token (data)
                email_hash = hashlib.sha256(new_email.encode()).hexdigest()
                if email_hash != token_dto.data:
                    return jsonify({'error': 'Invalid email hash'}), 400

            except Exception as e:
                return jsonify({'error': str(e)}), 400

            # try:
            #     decoded_token = current_app.extensions['jwt_manager'].decode(
            #         token,
            #         current_app.config['JWT_SECRET_KEY'],
            #         algorithms=['HS256'])
            #     email = decoded_token.get(
            #         'sub'
            #     )  # Récupère l'email actuel de l'utilisateur dans le token
            #     print(f"yzteeeeeeeeeee {decoded_token}")
            #     new_email = decoded_token.get(
            #         'new_email')  # Récupère le nouvel email dans les claims
            #     if not new_email:
            #         return jsonify({'error':
            #                         'New email is missing in token'}), 400
            # except current_app.extensions['jwt_manager'].ExpiredSignatureError:
            #     return jsonify({'error': 'Token has expired'}), 400
            # except current_app.extensions['jwt_manager'].InvalidTokenError:
            #     return jsonify({'error': 'Invalid token'}), 400

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
            user._email = new_email
            user_dto: UserDTO = user_to_dto(user)
            # print(f"user à mettre à jour : {email}")
            # print(f"donné maj : {user_dto}")
            updated_user = update_user_email(
                email, user_dto)  # Met à jour l'utilisateur en base de données

            updated_user_dto: UserDTO = user_to_dto(updated_user)
            # Retourner la réponse JSON
            return jsonify({
                'message': 'Email updated successfully',
                'user': updated_user_dto.to_dict()
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @account_blueprint.route('/update', methods=['PUT'])
    @jwt_required()
    def update_account():
        try:
            # Récupérer l'email de l'utilisateur connecté depuis le JWT
            email: str = get_jwt_identity()

            # Récupérer l'utilisateur en base de données
            user = get_user_by_email(email)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Récupérer les données envoyées dans la requête
            data: dict = request.get_json()
            if not data:
                return jsonify({'error':
                                'Invalid request, JSON required'}), 400

            # Initialiser la variable pour le token
            token = None

            # Vérifier si l'email est dans les données envoyées
            new_email = data.get('email')

            # Liste des champs à mettre à jour
            fields_to_update = {}
            # Initialiser le DTO avec les données actuelles
            user_dto: UserDTO = user_to_dto(user)

            # Comparer les autres champs et ajouter les modifications
            for field, value in data.items():
                # Conversion des champs de type date avant de les affecter
                if field in ['birth_at'] and isinstance(value, str):
                    try:
                        # Conversion de la chaîne de caractères en datetime.date ou datetime
                        if field == 'birth_at':
                            value = datetime.strptime(value, "%Y-%m-%d").date()
                        else:
                            value = datetime.strptime(
                                value, "%a, %d %b %Y %H:%M:%S GMT")
                    except ValueError:
                        return jsonify(
                            {'error': f"Invalid date format for {field}"}), 400

                # Ajouter à la liste des champs à mettre à jour
                if hasattr(user_dto, field) and getattr(user_dto,
                                                        field) != value:
                    fields_to_update[field] = value

            # Exclure certains champs qui ne doivent pas être modifiés
            for field in ["role", "login_at", "created_at"]:
                if field in fields_to_update:
                    del fields_to_update[field]

            # Si aucun champ à mettre à jour, retourner un message approprié
            if not fields_to_update:
                return jsonify({
                    'message': 'No changes to update.',
                    'user': user_dto.to_dict()
                }), 200

            # Appliquer les mises à jour
            for field, value in fields_to_update.items():
                setattr(user_dto, field, value)

            # Vérifier les changements avant de sauvegarder
            update_user(email=email, user_dto=user_dto)
            # Si l'email a été modifié, gérer la logique de validation du nouvel email
            if new_email and new_email != user._email:
                # Générer un salt unique pour la création du token
                salt = str(uuid.uuid4())  # Générer un salt unique

                # Supprimer les tokens périmés avant de créer un nouveau
                delete_expired_tokens()

                # Créer un hash de l'email pour pouvoir vérifier la correspondance plus tard
                email_hash = hashlib.sha256(new_email.encode()).hexdigest()

                # Générer un token JWT avec une expiration de 1 heure
                token = generate_token(user._email,
                                       expiration_hours=1,
                                       claims={"new_email": new_email},
                                       salt=salt)
                # token = generate_token(user_dto.email,
                #                        expiration_hours=1,
                #                        salt=salt)

                # Créer un TokenDTO avec le token, email hashé et salt
                token_dto = TokenDTO(
                    token=token,  # Le token généré
                    data=email_hash,  # Email hashé
                    salt=salt  # Le salt utilisé pour générer le token
                )

                # Persister le token en base de données avec l'email hashé et le salt utilisé
                insert_token(token_dto)

                # Générer l'URL de validation avec le token
                validation_url = f"{current_app.config['BASE_URL']}/profil/email_new?token={token_dto.token}"

                # Dictionnaire des variables pour le template
                context = {
                    'user_name': user_dto.firstname or 'Utilisateur',
                    'user_email': user_dto.email,
                    'validation_url': validation_url,
                    'current_year': datetime.now().year
                }

                # Envoi du mail avec le template
                send_email(subject="Confirmez votre inscription",
                           recipients=[user_dto.email],
                           template="mail/email_new.html",
                           context=context)

            # Sauvegarder les changements en base de données
            user: User = update_user(email, user_dto)

            update_user_dto: UserDTO = user_to_dto(user)

            user_dict: dict = update_user_dto.to_dict()

            if new_email:
                user_dict['new_email'] = new_email

            return jsonify({
                'success': 'User updated successfully',
                'user': user_dict
                # 'email_verification_token':
                # token  # Retourner le token si généré
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500
