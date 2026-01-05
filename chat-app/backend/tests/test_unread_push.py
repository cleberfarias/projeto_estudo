import pytest
import asyncio

import socket_handlers as socket_handlers
import contacts

@pytest.mark.asyncio
async def test_emit_unread_counts_for_user(monkeypatch):
    calls = []

    async def fake_emit(event, payload, room=None, **_kwargs):
        calls.append((event, payload, room))

    monkeypatch.setattr(socket_handlers.sio, 'emit', fake_emit)

    # Fake messages_collection methods
    async def fake_count_documents(query):
        assert query.get('contactId') == 'target_user'
        return 5

    async def fake_distinct(field, query):
        assert field == 'userId'
        return ['u1', 'u2']

    monkeypatch.setattr(socket_handlers, 'messages_collection', socket_handlers.messages_collection)
    monkeypatch.setattr(socket_handlers.messages_collection, 'count_documents', fake_count_documents)
    monkeypatch.setattr(socket_handlers.messages_collection, 'distinct', fake_distinct)

    # Simula usuário conectado
    socket_handlers.user_sessions['target_user'] = 'sid-123'

    res = await socket_handlers.emit_unread_counts_for_user('target_user')

    assert ('chat:unread-updated', {'unreadConversations': 2, 'unreadMessages': 5}, 'sid-123') in calls
    assert res['unreadConversations'] == 2
    assert res['unreadMessages'] == 5


@pytest.mark.asyncio
async def test_mark_conversation_read_emits(monkeypatch):
    # Monkeypatch emit_unread_counts_for_user
    calls = []
    async def fake_emit_counts(user_id):
        calls.append(user_id)

    monkeypatch.setattr(socket_handlers, 'emit_unread_counts_for_user', fake_emit_counts)

    # Monkeypatch db.messages.update_many used in contacts.mark_conversation_read
    class FakeResult:
        modified_count = 3

    class FakeMessages:
        async def update_many(self, *args, **kwargs):
            return FakeResult()

    monkeypatch.setattr(contacts, 'db', contacts.db)
    monkeypatch.setattr(contacts.db, 'messages', FakeMessages(), raising=False)

    res = await contacts.mark_conversation_read('contact-1', 'current-user')

    assert res['updated'] == 3
    # Verifica que emit_unread_counts_for_user foi chamado para current-user
    assert 'current-user' in calls


@pytest.mark.asyncio
async def test_publish_message_emits_unread(monkeypatch):
    calls = []

    async def fake_emit_counts(user_id):
        calls.append(user_id)

    monkeypatch.setattr(socket_handlers, 'emit_unread_counts_for_user', fake_emit_counts)

    # Simula publicação de mensagem com contact_id
    from bots.automations import publish_message

    # Mock sio.emit to capture message broadcast
    async def fake_sio_emit(event, payload, **_kwargs):
        # do nothing
        return None

    # Chama publish_message com contact_id => deve chamar emit_unread_counts_for_user(contact_id)
    await publish_message(fake_sio_emit, author='BotTest', text='Olá', contact_id='target_user')

    assert 'target_user' in calls


@pytest.mark.asyncio
async def test_webhook_persist_and_broadcast_emits_unread(monkeypatch):
    calls = []

    async def fake_emit_counts(user_id):
        calls.append(user_id)

    monkeypatch.setattr(socket_handlers, 'emit_unread_counts_for_user', fake_emit_counts)

    # Mock emit_to_user to be a coroutine
    async def fake_emit_to_user(payload, target_user_id=None):
        return None

    monkeypatch.setattr('backend.routers.webhooks.emit_to_user', fake_emit_to_user)

    # Call the internal helper directly
    from routers.webhooks import _persist_and_broadcast
    await _persist_and_broadcast('WA:12345', 'Hello webhook', target_user_id='target_user')

    assert 'target_user' in calls
