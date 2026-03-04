from app import db
from app.models import Property, Room
import requests
import os


USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5001")

def validate_owner(owner_id):
    """Vérifie que l'utilisateur existe dans le user-service"""
    try:
        response = requests.get(f"{USER_SERVICE_URL}/api/v1/users/{owner_id}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        # Si le user-service est inaccessible, on laisse passer pour ne pas bloquer le service
        return True


############# CRUD pour les biens immobiliers ################

def get_all_properties():
    return Property.query.all()

def get_property_by_id(property_id):
    return Property.query.filter_by(id=property_id).first()

def get_properties_by_city(city):
    return Property.query.filter_by(city=city).all()

def create_property(data):
    property = Property(
        name=data["name"],
        description=data.get("description"),
        type=data["type"],
        city=data["city"],
        owner_id=data["owner_id"],
    )
    db.session.add(property)
    db.session.commit()
    return property

def update_property(property, data):
    property.name = data.get("name", property.name)
    property.description = data.get("description", property.description)
    property.type = data.get("type", property.type)
    property.city = data.get("city", property.city)
    property.owner_id = data.get("owner_id", property.owner_id)
    db.session.commit()
    return property

def delete_property(property):
    db.session.delete(property)
    db.session.commit()

############# CRUD pour les pièces ################

def get_rooms_by_property(property_id):
    return Room.query.filter_by(property_id=property_id).all()

def get_room_by_id(room_id):
    return Room.query.filter_by(id=room_id).first()

def create_room(data, property_id):
    room = Room(
        property_id=property_id,
        name=data["name"],
        area_sqm=data.get("area_sqm"),
        description=data.get("description"),
    )
    db.session.add(room)
    db.session.commit()
    return room

def update_room(room, data):
    room.name = data.get("name", room.name)
    room.area_sqm = data.get("area_sqm", room.area_sqm)
    room.description = data.get("description", room.description)
    db.session.commit()
    return room

def delete_room(room):
    db.session.delete(room)
    db.session.commit()