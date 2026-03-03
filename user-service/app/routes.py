from flask import Blueprint, jsonify, request
from app.services import get_all_users, get_user_by_id, create_user, update_user, delete_user
from app.schemas import user_schema, users_schema

bp = Blueprint("users", __name__)

@bp.route("/")
def home():
    return jsonify({"message": "User service est en cours d'execution"}), 200

@bp.route("/users", methods=["GET"])
def get_users():
    users = get_all_users()
    return jsonify(users_schema.dump(users)), 200

@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    return jsonify(user_schema.dump(user)), 200

@bp.route("/users", methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not data or not data.get("first_name") or not data.get("last_name"):
        return jsonify({"error": "first_name et last_name sont obligatoires"}), 400
    user = create_user(data)
    return jsonify(user_schema.dump(user)), 201

@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    data = request.get_json()
    user = update_user(user, data)
    return jsonify(user_schema.dump(user)), 200

@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    delete_user(user)
    return jsonify({"message": "Utilisateur supprimé"}), 200