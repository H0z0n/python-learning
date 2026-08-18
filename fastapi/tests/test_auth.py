import uuid


def test_register_and_login(client):
    random_username = f"test_{uuid.uuid4().hex[:8]}"
    password = "123321"

    register_response = client.post("/register", json={"username": random_username, "password": password})
    assert register_response.status_code == 200

    login_response = client.post("/login", json={"username": random_username, "password": password})
    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client):
    random_username = f"test_{uuid.uuid4().hex[:8]}"
    password = "123321"

    client.post("/register", json={"username": random_username, "password": password})

    wrong_password_response = client.post("/login", json={"username": random_username, "password": "my-wrong-password1234567"})
    assert wrong_password_response.status_code == 401


def test_login_with_unnamed_username(client):
    unnamed_username = f"unnamed_{uuid.uuid4().hex[:8]}"
    password = "12345"

    login_response = client.post("/login", json={"username": unnamed_username, "password": password})
    assert login_response.status_code == 401


def test_register_user_already_exists(client):
    username = "Hozon"
    password = "12345"
    client.post("/register", json={"username": username, "password": password})

    register_response = client.post("/register", json={"username": username, "password": password})
    assert register_response.status_code == 400