from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import Property, Room

class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True

class PropertySchema(SQLAlchemyAutoSchema):
    rooms = fields.List(fields.Nested(RoomSchema))
    class Meta:
        model = Property
        load_instance = True

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)