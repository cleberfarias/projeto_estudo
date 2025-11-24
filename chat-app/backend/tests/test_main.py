def test_health(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
