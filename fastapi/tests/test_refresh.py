import uuid


def test_refresh_token(client):
    username = f"test_{uuid.uuid4().hex[:8]}"
    password = "123321"

    client.post("/register", json={"username": username, "password": password})
    login_response = client.post("/login", json={"username": username, "password": password})

    data = login_response.json()

    refresh_token = data["refresh_token"]

    refresh_response = client.post("/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200

    refresh_end_point_data = refresh_response.json()
    assert "access_token" in refresh_end_point_data
    assert "refresh_token" in refresh_end_point_data
    assert refresh_end_point_data["token_type"] == "bearer"


def test_refresh_token_fails(client):
    username = f"test_{uuid.uuid4().hex[:8]}"
    password = "123321"

    client.post("/register", json={"username": username, "password": password})
    login_response = client.post("/login", json={"username": username, "password": password})

    data = login_response.json()

    access_token = data["access_token"]

    refresh_response = client.post("/refresh", json={"refresh_token": access_token})
    assert refresh_response.status_code == 401