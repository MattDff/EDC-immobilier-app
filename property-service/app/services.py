from app import db
from app.models import Property, Room, PropertyType

############# CRUD for Property ################

def get_all_properties():
    return Property.query.all()

def get_property_by_id(property_id):
    return Property.query.get(property_id)

def get_properties_by_city(city):
    return Property.query.filter_by(city=city).all()

def create_property(data):
    property = Property(
        name=data["name"],
        description=data["description"],
        type=data["type"],
        city=data["city"],
        owner_id=data["owner_id"],
        rooms=data["rooms"],
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

############# CRUD for Room ################

def get_all_rooms():
    return Room.query.all()

def get_room_by_id(room_id):
    return Room.query.get(room_id)

def create_room(data):
    room = Room(
        property_id=data["property_id"],
        name=data["name"],
        area_sqm=data["area_sqm"],
        description=data["description"],
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

def delete_room(room_id):
    db.session.delete(room_id)
    db.session.commit()