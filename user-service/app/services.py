from app import db
from app.models import User
from datetime import datetime


def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def create_user(data):
    birth_date = None
    if data.get("birth_date"):
        birth_date = datetime.strptime(data["birth_date"], "%Y-%m-%d").date()

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=birth_date,
    )
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, data):
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.birth_date = data.get("birth_date", user.birth_date)
    db.session.commit()
    return user

def delete_user(user):
    db.session.delete(user)
    db.session.commit()