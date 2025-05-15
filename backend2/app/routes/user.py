from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{
        'email': u.email,
        'firstname': u.firstname,
        'lastname': u.lastname
    } for u in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur créé'}), 201