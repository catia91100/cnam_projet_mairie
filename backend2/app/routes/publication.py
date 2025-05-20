from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Category, Publication, User
import uuid

publication_bp = Blueprint('publication', __name__)


@publication_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    category = Category(
        name=data['name'],
        title=data.get('title'),
        description=data.get('description'),
        order=data.get('order'),
        ref_name=data.get('ref_name'),
        ref_parent=data.get('ref_parent')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Catégorie créée"}), 201


@publication_bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([
        {
            "name": cat.name,
            "title": cat.title,
            "description": cat.description,
            "order": cat.order,
            "ref_name": cat.ref_name,
            "ref_parent": cat.ref_parent
        } for cat in categories
    ]), 200


@publication_bp.route('/', methods=['POST'])
@jwt_required()
def create_publication():
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "Utilisateur non trouvé"}), 404

    publication = Publication(
        id=str(uuid.uuid4()),
        title=data['title'],
        description=data.get('description'),
        on_line=data.get('on_line', True),
        priority=data.get('priority', 0),
        ref_author=user.email,
        ref_category=data['ref_category']
    )
    db.session.add(publication)
    db.session.commit()
    return jsonify({"message": "Publication créée"}), 201


@publication_bp.route('/', methods=['GET'])
def list_publications():
    publications = Publication.query.all()
    return jsonify([
        {
            "id": pub.id,
            "title": pub.title,
            "description": pub.description,
            "on_line": pub.on_line,
            "priority": pub.priority,
            "created_at": pub.created_at.isoformat(),
            "updated_at": pub.updated_at.isoformat(),
            "ref_author": pub.ref_author,
            "ref_category": pub.ref_category
        } for pub in publications
    ]), 200