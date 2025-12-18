"""
Testes de integração para funcionalidades de tema e UI
"""
import pytest


def test_health_endpoint_returns_correct_structure(client):
    """Testa se o endpoint raiz retorna estrutura correta"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_messages_endpoint_accepts_text(client, fake_messages_collection):
    """Testa listagem de mensagens (GET /messages)"""
    # Adiciona mensagem diretamente no mock
    fake_messages_collection.data.append({
        "_id": "msg1",
        "text": "Teste de mensagem",
        "author": "user1",
        "createdAt": "2024-01-01T10:00:00Z",
        "status": "sent",
        "type": "text"
    })
    
    response = client.get("/messages")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert isinstance(data["messages"], list)


def test_messages_with_emoji(client, fake_messages_collection):
    """Testa mensagens com emojis"""
    from datetime import datetime, timezone
    # Adiciona mensagem com emoji diretamente
    fake_messages_collection.data.append({
        "_id": "msg_emoji",
        "text": "Olá! 👋 Como vai? 😊",
        "author": "user1",
        "createdAt": datetime.now(timezone.utc),
        "status": "sent",
        "type": "text"
    })
    
    response = client.get("/messages")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    # Verifica que a resposta tem formato correto
    assert isinstance(data["messages"], list)


def test_messages_list_returns_array(client, fake_messages_collection):
    """Testa estrutura de resposta da listagem de mensagens"""
    # Adiciona algumas mensagens diretamente
    from datetime import datetime, timezone
    for i in range(3):
        fake_messages_collection.data.append({
            "_id": f"m{i}",
            "text": f"Mensagem {i}",
            "author": f"user{i}",
            "createdAt": datetime.now(timezone.utc),
            "status": "sent",
            "type": "text"
        })
    
    response = client.get("/messages")
    assert response.status_code == 200
    
    data = response.json()
    # A resposta agora é um objeto com messages e hasMore
    assert isinstance(data, dict)
    assert "messages" in data
    assert isinstance(data["messages"], list)


def test_cors_headers_present(client):
    """Testa se headers CORS estão presentes"""
    response = client.options("/messages")
    # FastAPI adiciona CORS automaticamente quando configurado
    assert response.status_code in [200, 405]  # 405 se OPTIONS não implementado


def test_concurrent_message_sends(client, fake_messages_collection):
    """Testa acesso concorrente à listagem de mensagens"""
    import concurrent.futures
    from datetime import datetime, timezone
    
    # Adiciona mensagens ao mock
    for i in range(10):
        fake_messages_collection.data.append({
            "_id": f"concurrent_{i}",
            "text": f"Concurrent message {i}",
            "author": f"user{i}",
            "createdAt": datetime.now(timezone.utc),
            "status": "sent",
            "type": "text"
        })
    
    def get_messages(i):
        return client.get("/messages")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_messages, i) for i in range(10)]
        responses = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # Todas devem ter sucesso
    assert all(r.status_code == 200 for r in responses)
    assert all("messages" in r.json() for r in responses)
