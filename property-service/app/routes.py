from flask import Blueprint, jsonify, request
from app.services import get_all_properties, get_property_by_id, get_properties_by_city, create_property, update_property, delete_property, get_rooms_by_property, get_room_by_id, create_room, update_room, delete_room
from app.schemas import property_schema, properties_schema, room_schema, rooms_schema

bp = Blueprint("properties", __name__)

@bp.route("/")
def home():
    return jsonify({"message": "Property service is running"}), 200

############# Routes pour les biens immobiliers ################

@bp.route("/properties", methods=["GET"])
def get_properties():
    city = request.args.get("city")
    if city:
        properties = get_properties_by_city(city)
    else:
        properties = get_all_properties()
    return jsonify(properties_schema.dump(properties)), 200

@bp.route("/properties/<string:property_id>", methods=["GET"])
def get_property_route(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return jsonify({"error": "Propriété non trouvée"}), 404
    return jsonify(property_schema.dump(property)), 200

@bp.route("/properties", methods=["POST"])
def create_property_route():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("type") or not data.get("city") or not data.get("owner_id"):
        return jsonify({"error": "name, type, city et owner_id sont obligatoires"}), 400
    property = create_property(data)
    return jsonify(property_schema.dump(property)), 201

@bp.route("/properties/<string:property_id>", methods=["PUT"])
def update_property_route(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return jsonify({"error": "Propriété non trouvée"}), 404
    user_id = request.headers.get("X-User-Id")
    if not user_id or user_id != property.owner_id:
        return jsonify({"error": "Vous pouvez seulement modifier les propriétés dont vous êtes le propriétaire"}), 403
    data = request.get_json()
    property = update_property(property, data)
    return jsonify(property_schema.dump(property)), 200

@bp.route("/properties/<string:property_id>", methods=["DELETE"])
def delete_property_route(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return jsonify({"error": "Propriété non trouvée"}), 404
    user_id = request.headers.get("X-User-Id")
    if not user_id or user_id != property.owner_id:
        return jsonify({"error": "Vous pouvez seulement supprimer les propriétés dont vous êtes le propriétaire"}), 403
    delete_property(property)
    return jsonify({"message": "Propriété supprimée"}), 200

############# Routes pour les pièces ################

@bp.route("/properties/<string:property_id>/rooms", methods=["GET"])
def get_rooms_route(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return jsonify({"error": "Propriété non trouvée"}), 404
    rooms = get_rooms_by_property(property_id)
    return jsonify(rooms_schema.dump(rooms)), 200

@bp.route("/properties/<string:property_id>/rooms/<string:room_id>", methods=["GET"])
def get_room_route(property_id, room_id):
    room = get_room_by_id(room_id)
    if not room:
        return jsonify({"error": "Pièce non trouvée"}), 404
    return jsonify(room_schema.dump(room)), 200

@bp.route("/properties/<string:property_id>/rooms", methods=["POST"])
def create_room_route(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return jsonify({"error": "Propriété non trouvée"}), 404
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "name est obligatoire"}), 400
    room = create_room(data, property_id)
    return jsonify(room_schema.dump(room)), 201

@bp.route("/properties/<string:property_id>/rooms/<string:room_id>", methods=["PUT"])
def update_room_route(property_id, room_id):
    room = get_room_by_id(room_id)
    if not room:
        return jsonify({"error": "Pièce non trouvée"}), 404
    user_id = request.headers.get("X-User-Id")
    property = get_property_by_id(property_id)
    if not user_id or user_id != property.owner_id:
        return jsonify({"error": "Vous pouvez seulement modifier les propriétés dont vous êtes le propriétaire"}), 403
    data = request.get_json()
    room = update_room(room, data)
    return jsonify(room_schema.dump(room)), 200

@bp.route("/properties/<string:property_id>/rooms/<string:room_id>", methods=["DELETE"])
def delete_room_route(property_id, room_id):
    room = get_room_by_id(room_id)
    if not room:
        return jsonify({"error": "Pièce non trouvée"}), 404
    user_id = request.headers.get("X-User-Id")
    property = get_property_by_id(property_id)
    if not user_id or user_id != property.owner_id:
        return jsonify({"error": "Vous pouvez seulement modifier les propriétés dont vous êtes le propriétaire"}), 403
    delete_room(room)
    return jsonify({"message": "Pièce supprimée"}), 200