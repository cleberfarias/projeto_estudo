import os
import hmac
import hashlib
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Request
from bson import ObjectId

from database import messages_collection
from socket_handlers import emit_to_user
from socket_manager import sio
from storage import presign_get

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
WA_OWNER_USER_ID = os.getenv("WA_OWNER_USER_ID")


async def _persist_and_broadcast(author: str, text: str, target_user_id: Optional[str] = None):
    doc = {
        "_id": ObjectId(),
        "author": author,
        "text": text,
        "type": "text",
        "status": "delivered",
        "createdAt": datetime.now(),
        "contactId": target_user_id if target_user_id else None,
        "userId": author if target_user_id else None
    }
    await messages_collection.insert_one(doc)
    payload = {
        "id": str(doc["_id"]),
        "author": author,
        "text": text,
        "type": "text",
        "status": "delivered",
        "timestamp": int(doc["createdAt"].timestamp() * 1000)
    }
    if target_user_id:
        payload["contactId"] = target_user_id
        payload["userId"] = author
    emit_task = emit_to_user(payload, target_user_id)
    if emit_task:
        await emit_task


@router.get("/meta")
async def webhook_meta_verify(
    mode: str = Query(..., alias="hub.mode"),
    challenge: str = Query(..., alias="hub.challenge"),
    verify_token: str = Query(..., alias="hub.verify_token")
):
    META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "")
    if mode == "subscribe" and verify_token == META_VERIFY_TOKEN:
        return int(challenge) if challenge.isdigit() else challenge
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/meta")
async def webhook_meta_receive(request: Request):
    raw_body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256")
    try:
        from meta import verify_meta_signature
        if not verify_meta_signature(raw_body, signature_header):
            raise HTTPException(status_code=403, detail="Invalid signature")
    except ImportError:
        print("⚠️  meta.py não encontrado, pulando verificação de assinatura")

    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            sender_id = msg.get("sender", {}).get("id")
            text_content = msg.get("message", {}).get("text")
            if sender_id and text_content:
                author = f"FB:{sender_id}"
                await _persist_and_broadcast(author, text_content, target_user_id=WA_OWNER_USER_ID)
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                sender = msg.get("from")
                text_content = msg.get("text", {}).get("body")
                if sender and text_content:
                    platform = change.get("field", "unknown")
                    if platform == "messages":
                        if sender.isdigit():
                            author = f"WA:{sender}"
                        else:
                            author = f"IG:{sender}"
                    else:
                        author = f"{platform}:{sender}"
                    await _persist_and_broadcast(author, text_content, target_user_id=WA_OWNER_USER_ID)
    return {"status": "ok"}


@router.post("/wppconnect")
async def webhook_wppconnect_receive(request: Request):
    raw_body = await request.body()
    signature_header = request.headers.get("x-webhook-signature")
    WPP_WEBHOOK_SECRET = os.getenv("WPP_WEBHOOK_SECRET", "")
    if WPP_WEBHOOK_SECRET and signature_header:
        expected_signature = hmac.new(
            WPP_WEBHOOK_SECRET.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature_header, expected_signature):
            print("❌ Webhook WPPConnect: assinatura inválida")
            raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if data.get("event") == "message":
        msg_data = data.get("data", {})
        sender_name = msg_data.get("fromName") or msg_data.get("from", "unknown")
        text_content = msg_data.get("contentText") or msg_data.get("body", "")
        if text_content:
            author = f"WA(dev):{sender_name}"
            await _persist_and_broadcast(author, text_content, target_user_id=WA_OWNER_USER_ID)

    return {"status": "ok"}
