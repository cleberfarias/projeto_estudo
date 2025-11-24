def test_messages_requires_auth():
    from backend import main
    from deps import get_current_user_id
    main.app.dependency_overrides = {}  # não injeta usuário
    from fastapi.testclient import TestClient
    client = TestClient(main.app)
    resp = client.get("/messages")
    assert resp.status_code == 401
    # restaura override vazio para outros testes
    main.app.dependency_overrides = {}


def test_messages_filters_by_user(client):
    resp = client.get("/messages")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["messages"]) == 1
    assert data["messages"][0]["author"] == "Alice"
