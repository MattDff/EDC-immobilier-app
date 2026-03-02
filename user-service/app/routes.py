from flask import Blueprint, jsonify

bp = Blueprint("users", __name__)

@bp.route("/")
def home():
    return jsonify({"message": "API is running"})