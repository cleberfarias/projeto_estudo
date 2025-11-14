"""Módulo de automações e agendamento de mensagens."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timezone
from typing import Callable, Any
from database import db

scheduler = AsyncIOScheduler()
automations_col = db.automations
messages_col = db.messages

BOT_AUTHOR = "Bot"


async def publish_message(
    sio_emit: Callable[[str, dict[str, Any]], Any],
    author: str,
    text: str,
    type_: str = "text"
) -> None:
    """
    Publica uma mensagem no chat e persiste no banco.
    
    Args:
        sio_emit: Função de emissão do Socket.IO
        author: Nome do autor da mensagem
        text: Conteúdo da mensagem
        type_: Tipo da mensagem (padrão: "text")
    """
    now = datetime.now(timezone.utc)
    doc = {
        "author": author,
        "text": text,
        "type": type_,
        "status": "sent",
        "createdAt": now
    }
    result = await messages_col.insert_one(doc)
    
    await sio_emit("chat:new-message", {
        "id": str(result.inserted_id),
        "author": author,
        "text": text,
        "type": type_,
        "status": "sent",
        "timestamp": int(now.timestamp() * 1000)
    })


async def _create_cron_job(
    sio_emit: Callable[[str, dict[str, Any]], Any],
    automation: dict[str, Any]
) -> None:
    """Cria um job cron para uma automação."""
    await publish_message(
        sio_emit,
        author=BOT_AUTHOR,
        text=automation["payload"]["text"]
    )


async def load_and_schedule_all(sio_emit: Callable[[str, dict[str, Any]], Any]) -> None:
    """
    Carrega e agenda todas as automações do tipo cron habilitadas.
    
    Args:
        sio_emit: Função de emissão do Socket.IO
    """
    async for automation in automations_col.find({"enabled": True, "type": "cron"}):
        # Validação
        if "spec" not in automation or "cron" not in automation["spec"]:
            continue
        if "payload" not in automation or "text" not in automation["payload"]:
            continue
            
        cron_expr = automation["spec"]["cron"]
        job_id = f"auto:{automation['_id']}"
        
        # Evita duplicar
        if scheduler.get_job(job_id):
            continue
        
        try:
            trigger = CronTrigger.from_crontab(cron_expr)
            scheduler.add_job(
                _create_cron_job,
                trigger=trigger,
                id=job_id,
                replace_existing=True,
                args=[sio_emit, automation]
            )
        except Exception as e:
            print(f"❌ Erro ao agendar automação {job_id}: {e}")


def start_scheduler() -> None:
    """Inicia o scheduler se ainda não estiver rodando."""
    if not scheduler.running:
        scheduler.start()


async def handle_keyword_if_matches(
    sio_emit: Callable[[str, dict[str, Any]], Any],
    text: str
) -> None:
    """
    Verifica se o texto corresponde a uma keyword e dispara automação.
    
    Args:
        sio_emit: Função de emissão do Socket.IO
        text: Texto da mensagem para verificar
    """
    keyword = text.strip().lower()
    automation = await automations_col.find_one({
        "enabled": True,
        "type": "keyword",
        "spec.keyword": keyword
    })
    
    if automation and "payload" in automation and "text" in automation["payload"]:
        await publish_message(
            sio_emit,
            author=BOT_AUTHOR,
            text=automation["payload"]["text"]
        )
