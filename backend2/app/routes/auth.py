from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db, bcrypt
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(login=login).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify({
        "message": "Utilisateur bien connecté",
        "access_token": access_token,
        "prenom": user.firstname,
        "nom": user.lastname,
        "email": user.email,
        "role": user.role
    }), 200
    return jsonify({"msg": "Identifiants invalides"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    user = User(
        email=data['email'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        birth_date=data['birth_date'],
        login=data['login'],
        password=hashed_password,
        role=data.get('role')
    )

    db.session.add(user)
    db.session.commit()

    # Création du token JWT immédiatement après l'inscription
    access_token = create_access_token(identity=user.email)

    return jsonify({
        "message": "Utilisateur enregistré",
        "access_token": access_token,
        "prenom": user.firstname,
        "nom": user.lastname,
        "email": user.email,
        "role": user.role
    }), 201

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"msg": "Utilisateur non trouvé"}), 404

    return jsonify({
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "birth_date": user.birth_date.isoformat(),
        "login": user.login,
        "role": user.role
    }), 200