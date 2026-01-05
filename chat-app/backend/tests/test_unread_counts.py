import pytest
from bson import ObjectId

@pytest.mark.asyncio
async def test_unread_count_requires_authentication(client):
    response = client.get('/contacts/unread-count')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unread_count_returns_counts(monkeypatch):
    """Testa que o endpoint retorna o número de conversas não-lidas e mensagens não-lidas"""
    # Fake messages collection
    class FakeMessagesCollection:
        async def count_documents(self, query):
            # Deve contar mensagens onde contactId == current_user
            return 5

        async def distinct(self, field, query):
            # Retorna lista de userIds que enviaram mensagens não-lidas
            return ["507f1f77bcf86cd799439012", "507f1f77bcf86cd799439013"]

    class FakeDb:
        def __init__(self):
            self.messages = FakeMessagesCollection()

    import contacts
    monkeypatch.setattr("contacts.db", FakeDb())

    # Chama a função diretamente (sem Request) passando o user id
    result = await contacts.unread_counts("507f1f77bcf86cd799439001")

    assert result["unreadMessages"] == 5
    assert result["unreadConversations"] == 2
