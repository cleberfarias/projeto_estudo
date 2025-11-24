from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

from database import db
from deps import get_current_user_id
from bots.automations import load_and_schedule_all
from socket_manager import sio

router = APIRouter(prefix="/automations", tags=["automations"])
automations_col = db.automations


class AutomationIn(BaseModel):
    name: str
    type: str  # "cron" | "keyword"
    spec: dict
    payload: dict
    enabled: bool = True


@router.post("")
async def create_automation(body: AutomationIn, _current_user_id: str = Depends(get_current_user_id)):
    doc = body.model_dump()
    doc["createdAt"] = datetime.now(timezone.utc)
    result = await automations_col.insert_one(doc)
    await load_and_schedule_all(sio.emit)
    return {"id": str(result.inserted_id), "message": "Automação criada com sucesso"}


@router.get("")
async def list_automations(_current_user_id: str = Depends(get_current_user_id)):
    automations = []
    async for automation in automations_col.find():
        automation["id"] = str(automation["_id"])
        del automation["_id"]
        automations.append(automation)
    return automations


@router.patch("/{id}/toggle")
async def toggle_automation(id: str, enabled: bool = Query(...), _current_user_id: str = Depends(get_current_user_id)):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "ID inválido")
    _id = ObjectId(id)
    result = await automations_col.update_one({"_id": _id},{"$set": {"enabled": enabled}})
    if result.matched_count == 0:
        raise HTTPException(404, "Automação não encontrada")
    await load_and_schedule_all(sio.emit)
    return {"ok": True, "message": f"Automação {'ativada' if enabled else 'desativada'}"}


@router.delete("/{id}")
async def delete_automation(id: str, _current_user_id: str = Depends(get_current_user_id)):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "ID inválido")
    _id = ObjectId(id)
    result = await automations_col.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Automação não encontrada")
    await load_and_schedule_all(sio.emit)
    return {"ok": True, "message": "Automação removida com sucesso"}
