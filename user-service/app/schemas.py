from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)