import uuid
from app import db


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)
    rooms = db.relationship("Room", backref="property", lazy=True)

    # Fonction pour afficher lisiblement dans le terminal quand on debug
    def __repr__(self):
        return f"<Property {self.name} {self.city}>"


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = db.Column(db.String(36), db.ForeignKey("properties.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    area_sqm = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Fonction pour afficher lisiblement dans le terminal quand on debug
    def __repr__(self):
        return f"<Room {self.name}>"