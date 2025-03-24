from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from utils.utils import generate_psw, send_email, generate_token, hash_password, decode_token_custom
from dtos.user_dto import UserDTO
from services.user_service import insert_user, verify_login, get_user_by_email, update_login_at
from services.token_service import insert_token, delete_token, delete_expired_tokens, check_token_exists
from datetime import datetime, timezone
import hashlib, uuid
from dtos.token_dto import TokenDTO

security_blueprint = Blueprint("security", __name__)


class Security:

    @security_blueprint.route('/inscription', methods=['POST'])
    def inscription():
        try:
            # Récupérer les données du corps de la requête
            data = request.json

            # Vérifier si un utilisateur existe déjà avec cet email
            existing_user = get_user_by_email(data.get('email'))
            if existing_user:
                return jsonify({'error': 'Email already in use'}), 409

            # Générer un mot de passe si nécessaire
            data['password'] = generate_psw()

            # Validation Pydantic du DTO
            user_dto = UserDTO(**data)

            # Générer un salt unique pour la création du token
            salt = str(uuid.uuid4())  # Générer un salt unique

            # Supprimer les tokens périmés avant de créer un nouveau
            delete_expired_tokens()

            # Créer un hash de l'email pour pouvoir vérifier la correspondance plus tard
            email_hash = hashlib.sha256(user_dto.email.encode()).hexdigest()

            # Générer un token JWT avec une expiration de 1 heure
            token = generate_token(user_dto.email,
                                   expiration_hours=1,
                                   salt=salt)

            # Créer un TokenDTO avec le token, email hashé et salt
            token_dto = TokenDTO(
                token=token,  # Le token généré
                data=email_hash,  # Email hashé
                salt=salt  # Le salt utilisé pour générer le token
            )

            # Persister le token en base de données avec l'email hashé et le salt utilisé
            insert_token(token_dto)

            # Générer l'URL de validation avec le token
            validation_url = f"{current_app.config['BASE_URL']}/completer-inscription/?token={token_dto.token}"

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

            # Retourner une réponse réussie avec le DTO
            return jsonify({'email': user_dto.email}), 200

        except ValidationError as e:
            return jsonify({
                'error': 'Invalid data',
                'details': e.errors()
            }), 400

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @security_blueprint.route('/validation-email', methods=['GET'])
    def validate_token():
        try:
            # Récupérer le token depuis l'URL
            token = request.args.get('token')
            if not token:
                return jsonify({'error': 'Token is missing'}), 400

            # Vérifier si le token existe en base avec check_token_exists
            token_dto = check_token_exists(token)
            if not token_dto:
                return jsonify({'error': 'Invalid or expired token'}), 400

            # Supprimer le token après utilisation avec delete_token
            delete_token(token)

            # Décoder le token avec le salt
            try:
                decoded_token = decode_token_custom(token, token_dto.salt)
                email = decoded_token.get('sub')
                if not email:
                    return jsonify({'error': 'Invalid token'}), 400

                # Vérifier la correspondance avec l'email hashé stocké dans le token (data)
                email_hash = hashlib.sha256(email.encode()).hexdigest()
                if email_hash != token_dto.data:
                    return jsonify({'error': 'Invalid email hash'}), 400

            except Exception as e:
                return jsonify({'error': str(e)}), 400

            # Générer un nouveau token valide pour 1 heure en utilisant generate_token

            salt = str(uuid.uuid4())  # Générer un salt unique

            new_token = generate_token(email, expiration_hours=1, salt=salt)
            new_token_dto: TokenDTO = TokenDTO(token=new_token,
                                               data=email_hash,
                                               salt=salt)

            # Sauvegarder le nouveau token en base de données
            insert_token(new_token_dto)

            # Retourner la réponse JSON avec le nouveau token
            return jsonify({
                'verification': True,
                'email': email,
                'token': new_token_dto.token
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @security_blueprint.route('/completer-inscription', methods=['POST'])
    def completer_inscription():
        try:
            # Récupérer les données du corps de la requête
            data = request.json
            token = data.get(
                'token')  # Récupérer le token envoyé dans la requête
            if not token:
                return jsonify({'error': 'Token is missing'}), 400

            # Vérifier si le token existe en base avec check_token_exists
            token_dto = check_token_exists(token)
            if not token_dto:
                return jsonify({'error': 'Invalid or expired token'}), 400

            # Supprimer le token après utilisation avec delete_token
            delete_token(token)

            # Décoder le token pour récupérer l'email
            try:
                decoded_token = decode_token_custom(token, token_dto.salt)
                email = decoded_token.get('sub')
                if not email:
                    return jsonify({'error': 'Invalid token'}), 400

                # Vérifier la correspondance avec l'email hashé stocké dans le token (data)
                email_hash = hashlib.sha256(email.encode()).hexdigest()
                if email_hash != token_dto.data:
                    return jsonify({'error': 'Invalid email hash'}), 400

            except Exception as e:
                return jsonify({'error': str(e)}), 400

            # Vérifier si l'utilisateur existe déjà dans la base
            # Si l'utilisateur existe déjà, on ne l'insère pas à nouveau
            existing_user = get_user_by_email(email)
            if existing_user:
                return jsonify({'error': 'User already exists'}), 409

            # Récupérer les données de l'utilisateur envoyées dans la requête
            user_data = data.get('user')
            if not user_data:
                return jsonify({'error': 'User data is missing'}), 400

            # Créer un DTO utilisateur avec les informations fournies
            user_dto = UserDTO(
                email=email,
                password=user_data.get('password'),
                firstname=user_data.get('firstname'),
                lastname=user_data.get('lastname'),
                birth_at=user_data.get('birth_at'),
                login_at=datetime.now(timezone.utc)  # Date de connexion
            )

            # Hacher le mot de passe avant l'insertion
            user_dto.password = hash_password(user_dto.password)

            # Insérer l'utilisateur dans la base de données avec insert_user
            insert_user(user_dto)
            # print(user_dto)

            # Retourner une réponse JSON indiquant que l'inscription est complète
            return jsonify({
                'message': 'Inscription complétée avec succès',
                'email': email
            }), 200

        except ValidationError as e:
            return jsonify({
                'error': 'Invalid data',
                'details': e.errors()
            }), 400

        except IntegrityError as e:
            return jsonify({
                'error': 'Database constraint violation',
                'details': str(e)
            }), 409

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @security_blueprint.route('/login', methods=['POST'])
    def login():
        try:
            # Récupérer les données du corps de la requête
            data = request.json
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({'error':
                                'Email and password are required'}), 400

            # Vérifier si l'utilisateur existe et si le mot de passe est valide
            if not verify_login(email, password):
                return jsonify({'error': 'Invalid email or password'}), 400

            # Récupérer l'utilisateur depuis la base de données
            user = get_user_by_email(email)
            if not user:
                return jsonify({'error': 'Invalid email or password'}), 400

            # Générer un token JWT avec une expiration de 1 heure
            token = generate_token(user._email, expiration_hours=1)

            # # Sauvegarder le token en base de données
            # insert_token(token_dto.token)

            # Retourner la réponse JSON avec le token

            update_login_at(email)
            # return jsonify({
            #     'message': 'Login successful',
            #     'email': user._email,
            #     # 'role' : user._role||'ROLE_USER'
            #     'token': token
            # }), 200
            return jsonify({
                "message": "Login successful",
                "user": {
                    "lastname": user._lastname[0],
                    "token": token
                },
            }), 200

        except IntegrityError as e:
            return jsonify({
                'error': 'Database constraint violation',
                'details': str(e)
            }), 409

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500
