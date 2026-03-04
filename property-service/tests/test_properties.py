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


def test_get_properties_empty(client):
    response = client.get("/api/v1/properties")
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_property(client):
    response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Bel Appart"
    assert data["type"] == "apartment"
    assert data["city"] == "Paris"
    assert data["owner_id"] == "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"

def test_create_property_missing_fields(client):
    response = client.post("/api/v1/properties", json={"name": "Joli Appart"})
    assert response.status_code == 400

def test_get_property_not_found(client):
    response = client.get("/api/v1/properties/uuid-inexistant")
    assert response.status_code == 404

def test_get_properties_by_city(client):
    client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    response = client.get("/api/v1/properties?city=Paris")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["city"] == "Paris"

def test_create_room(client):
    property_response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    property_id = property_response.get_json()["id"]

    response = client.post(f"/api/v1/properties/{property_id}/rooms", json={
        "name": "Salon",
        "area_sqm": 25.0
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Salon"
    assert data["area_sqm"] == 25.0

def test_get_rooms(client):
    property_response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    property_id = property_response.get_json()["id"]

    client.post(f"/api/v1/properties/{property_id}/rooms", json={
        "name": "Salon",
        "area_sqm": 25.0
    })

    response = client.get(f"/api/v1/properties/{property_id}/rooms")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_update_property(client):
    property_response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    property_id = property_response.get_json()["id"]
    response = client.put(f"/api/v1/properties/{property_id}", json={"name": "Nouvel Appart"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Nouvel Appart"

def test_delete_property(client):
    property_response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    property_id = property_response.get_json()["id"]
    response = client.delete(f"/api/v1/properties/{property_id}")
    assert response.status_code == 200

def test_update_room(client):
    property_response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    property_id = property_response.get_json()["id"]
    room_response = client.post(f"/api/v1/properties/{property_id}/rooms", json={
        "name": "Salon",
        "area_sqm": 25.0
    })
    room_id = room_response.get_json()["id"]
    response = client.put(f"/api/v1/properties/{property_id}/rooms/{room_id}", json={"name": "Grande Salle"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Grande Salle"

def test_delete_room(client):
    property_response = client.post("/api/v1/properties", json={
        "name": "Bel Appart",
        "type": "apartment",
        "city": "Paris",
        "owner_id": "6bd019c9-ffe4-44f4-ba14-26ca4717dba4"
    })
    property_id = property_response.get_json()["id"]
    room_response = client.post(f"/api/v1/properties/{property_id}/rooms", json={
        "name": "Salon",
        "area_sqm": 25.0
    })
    room_id = room_response.get_json()["id"]
    response = client.delete(f"/api/v1/properties/{property_id}/rooms/{room_id}")
    assert response.status_code == 200
