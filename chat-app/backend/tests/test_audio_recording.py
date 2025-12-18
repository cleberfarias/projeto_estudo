"""
Testes para funcionalidade de gravação de áudio
"""
import pytest
from io import BytesIO


def test_audio_upload_grant(client):
    """Testa concessão de upload para arquivo de áudio"""
    response = client.post("/uploads/grant", json={
        "filename": "audio_recording.webm",
        "mimetype": "audio/webm",
        "size": 1024 * 500  # 500KB
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
    assert "putUrl" in data
    assert data["key"].endswith(".webm")


def test_audio_upload_confirm(client, fake_messages_collection):
    """Testa confirmação de upload de áudio"""
    # Grant primeiro
    grant_resp = client.post("/uploads/grant", json={
        "filename": "voice_note.webm",
        "mimetype": "audio/webm",
        "size": 1024 * 300
    })
    assert grant_resp.status_code == 200
    grant = grant_resp.json()
    
    # Confirm
    confirm_resp = client.post("/uploads/confirm", json={
        "key": grant["key"],
        "filename": "voice_note.webm",
        "mimetype": "audio/webm",
        "author": "user123"
    })
    
    assert confirm_resp.status_code == 200
    data = confirm_resp.json()
    assert data["ok"] is True
    assert data["message"]["attachment"]["mimetype"] == "audio/webm"
    assert data["message"]["type"] == "audio"  # type está na mensagem, não no attachment
    
    # Verifica se foi salvo
    saved = any(
        doc.get("attachment", {}).get("filename") == "voice_note.webm"
        for doc in fake_messages_collection.data
    )
    assert saved


def test_audio_size_limit(client):
    """Testa limite de tamanho para áudio (5 minutos = ~10MB)"""
    # Arquivo de tamanho razoável (5MB)
    response = client.post("/uploads/grant", json={
        "filename": "long_audio.webm",
        "mimetype": "audio/webm",
        "size": 1024 * 1024 * 5
    })
    
    # Deve aceitar
    assert response.status_code == 200
    assert "key" in response.json()


def test_audio_invalid_mimetype(client):
    """Testa upload com mimetype inválido - executáveis são bloqueados"""
    response = client.post("/uploads/grant", json={
        "filename": "test.exe",
        "mimetype": "application/x-msdownload",
        "size": 1024
    })
    
    # Deve bloquear executáveis
    assert response.status_code == 400


def test_multiple_audio_uploads(client, fake_messages_collection):
    """Testa múltiplos uploads de áudio sequenciais"""
    for i in range(3):
        # Grant
        grant_resp = client.post("/uploads/grant", json={
            "filename": f"audio_{i}.webm",
            "mimetype": "audio/webm",
            "size": 1024 * 100
        })
        assert grant_resp.status_code == 200
        grant = grant_resp.json()
        
        # Confirm
        confirm_resp = client.post("/uploads/confirm", json={
            "key": grant["key"],
            "filename": f"audio_{i}.webm",
            "mimetype": "audio/webm",
            "author": f"user{i}"
        })
        assert confirm_resp.status_code == 200
    
    # Verifica se todos foram salvos
    audio_count = sum(
        1 for doc in fake_messages_collection.data
        if doc.get("type") == "audio" and "attachment" in doc
    )
    assert audio_count == 3


def test_audio_message_structure(client, fake_messages_collection):
    """Testa estrutura correta da mensagem com áudio"""
    # Grant e Confirm
    grant_resp = client.post("/uploads/grant", json={
        "filename": "test_audio.webm",
        "mimetype": "audio/webm",
        "size": 1024 * 200
    })
    grant = grant_resp.json()
    
    confirm_resp = client.post("/uploads/confirm", json={
        "key": grant["key"],
        "filename": "test_audio.webm",
        "mimetype": "audio/webm",
        "author": "test_user"
    })
    
    data = confirm_resp.json()
    message = data["message"]
    
    # Verifica estrutura
    assert "id" in message
    assert "author" in message
    assert "timestamp" in message
    assert "attachment" in message
    assert message["type"] == "audio"  # type está na mensagem, não no attachment
    
    attachment = message["attachment"]
    assert attachment["filename"] == "test_audio.webm"
    assert attachment["mimetype"] == "audio/webm"
    assert "url" in message  # URL está no nível da mensagem
    assert attachment["key"]  # Key do S3
