def test_wrong_weapons_id(client):
    response = client.get("/weapons/99999")
    assert response.status_code == 404