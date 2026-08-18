import uuid


def test_create_player(client):
    username = f"test_{uuid.uuid4().hex[:8]}"
    password = "123321"

    client.post("/register", json={"username": username, "password": password})
    login_response = client.post("/login", json={"username": username, "password": password})

    access_token = login_response.json()["access_token"]

    players_response = client.post(
        "/players", 
        json={"name": "MyNewCharacter", "hp": 150, "level": 5}, 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert players_response.status_code == 200


def test_create_player_fails(client):
    players_response = client.post("/players", json={"name": "MyNewCharacter", "hp": 150, "level": 5})
    assert players_response.status_code == 401


def test_get_player_fails(client):
    get_players_response = client.get("/players/9999999999")
    assert get_players_response.status_code == 404


def test_delete_player_fails(client):
    delete_players_response = client.delete("/players/9999999999")
    assert delete_players_response.status_code == 404