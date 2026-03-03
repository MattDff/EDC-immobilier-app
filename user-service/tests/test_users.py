import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_get_users_empty(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_user(client):
    response = client.post("/api/v1/users", json={
        "first_name": "Jean",
        "last_name": "Dupont",
        "birth_date": "1990-01-15"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["first_name"] == "Jean"
    assert data["last_name"] == "Dupont"

def test_create_user_missing_fields(client):
    response = client.post("/api/v1/users", json={"first_name": "Jean"})
    assert response.status_code == 400

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/uuid-inexistant")
    assert response.status_code == 404

def test_update_user(client):
    create_response = client.post("/api/v1/users", json={
        "first_name": "Jean",
        "last_name": "Dupont"
    })
    user_id = create_response.get_json()["id"]
    response = client.put(f"/api/v1/users/{user_id}", json={"first_name": "Pierre"})
    assert response.status_code == 200
    assert response.get_json()["first_name"] == "Pierre"

def test_delete_user(client):
    create_response = client.post("/api/v1/users", json={
        "first_name": "Jean",
        "last_name": "Dupont"
    })
    user_id = create_response.get_json()["id"]
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200