import pytest
from datetime import datetime
from bson import ObjectId


@pytest.mark.asyncio
async def test_create_contact_inserts_document(monkeypatch):
    created = {"id": None}

    class FakeResult:
        def __init__(self, inserted_id):
            self.inserted_id = inserted_id

    class FakeContactsCollection:
        async def insert_one(self, doc):
            created["id"] = str(ObjectId())
            return FakeResult(ObjectId(created["id"]))

    class FakeDb:
        def __init__(self):
            self.contacts = FakeContactsCollection()

    import contacts
    monkeypatch.setattr("contacts.db", FakeDb())

    from contacts import create_contact

    # Simula criação
    result = await create_contact(type("D", (), {"name": "Cli Test", "email": None, "phone": "+5511999999999"})(), "user1")
    assert "id" in result


@pytest.mark.asyncio
async def test_list_contacts_includes_external_contacts(monkeypatch):
    # Simula sem usuários do sistema, apenas contatos externos
    fake_users = []

    class FakeUsersCollection:
        def find(self, query, projection):
            class C:
                async def to_list(self, n):
                    return fake_users
            return C()

    last_msg_time = datetime(2025, 1, 1, 12, 0, 0)
    fake_message = {
        "_id": ObjectId(),
        "text": "Mensagem externa",
        "createdAt": last_msg_time
    }

    class FakeContactsCursor:
        async def to_list(self, n):
            return [{
                "_id": ObjectId("507f1f77bcf86cd799439099"),
                "name": "Contato Externo",
                "phone": "+5511999999999",
                "createdBy": "user1"
            }]

    class FakeContactsCollection:
        def find(self, query):
            return FakeContactsCursor()

    class FakeMessagesCollection:
        async def find_one(self, query, sort=None):
            return fake_message

    class FakeDb:
        def __init__(self):
            self.users = FakeUsersCollection()
            self.contacts = FakeContactsCollection()
            self.messages = FakeMessagesCollection()

    import contacts
    monkeypatch.setattr("contacts.db", FakeDb())

    from contacts import list_contacts
    result = await list_contacts("user1")

    assert len(result) == 1
    assert result[0].name == "Contato Externo"
    assert result[0].lastMessage == "Mensagem externa"
    assert result[0].lastMessageTime == int(last_msg_time.timestamp() * 1000)
