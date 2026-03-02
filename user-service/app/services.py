from app import db
from app.models import User
from sqlalchemy.sql.functions import user


def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(data):
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data['birth_date'],
    )
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, data):
    user.first_name = data.get("firt_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.birth_date = data.get("birth_date", user.birth_date)
    db.session.commit()
    return user

def delete_user(user_id):
    db.session.delete(user)
    db.session.commit()