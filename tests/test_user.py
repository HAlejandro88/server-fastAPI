from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "John Doe", "email": "john8@example.com", "password": "password"})
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}

def get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "name" in response.json()[0]  # Verifica que el primer usuario tenga un campo "name"
    assert "email" in response.json()[0]
    assert response.json() > 0