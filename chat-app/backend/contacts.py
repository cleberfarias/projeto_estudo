"""
Gerenciamento de contatos e conversas
"""
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Request
from bson import ObjectId
from bson.errors import InvalidId
from database import db
from deps import get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/contacts", tags=["contacts"])


# ============================================================================
# MODELS
# ============================================================================

class Contact(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    avatar: Optional[str] = None
    lastMessage: Optional[str] = None
    lastMessageTime: Optional[int] = None
    unreadCount: int = 0
    online: bool = False

class ContactCreate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None


@router.post("/", status_code=201)
async def create_contact(data: ContactCreate, current_user_id: str = Depends(get_current_user_id)):
    """
    Cria um contato externo (ex: cliente por telefone)
    """
    doc = {
        "name": data.name or data.email or data.phone or "Contato",
        "email": data.email,
        "phone": data.phone,
        "createdBy": current_user_id,
        "createdAt": datetime.utcnow()
    }
    result = await db.contacts.insert_one(doc)
    return {"id": str(result.inserted_id)}

class ConversationMessage(BaseModel):
    id: str
    author: str
    text: str
    timestamp: int
    type: str = "text"
    status: Optional[str] = None
    userId: Optional[str] = None  # 🆕 ID do remetente
    contactId: Optional[str] = None  # 🆕 ID do destinatário
    attachment: Optional[dict] = None
    url: Optional[str] = None

# ============================================================================
# ROUTES
# ============================================================================

@router.get("/", response_model=List[Contact])
async def list_contacts(current_user_id: str = Depends(get_current_user_id), request: Request = None):
    """
    Lista todos os usuários cadastrados como contatos
    (compatibilidade com mensagens antigas sem contactId)
    """
    # Se chamada via HTTP, 'request' estará presente e devemos exigir header Authorization
    exclude_seeds = False
    if request is not None:
        if not request.headers.get("Authorization") and not request.headers.get("authorization"):
            raise HTTPException(status_code=401, detail="Token ausente")
        exclude_seeds = True

    # Retorna usuários do sistema (exceto o próprio)
    try:
        id_filter = {"_id": {"$ne": ObjectId(current_user_id)}}
    except InvalidId:
        id_filter = {"_id": {"$ne": current_user_id}}

    users = await db.users.find(id_filter, {"password": 0}).to_list(None)
    
    contacts = []

    def is_seed_user(u: dict) -> bool:
        """Heurística para identificar usuários de seed/teste.
        Exclui e-mails com 'test' ou 'example.com', e nomes com 'Test' ou que começam com 'New'.
        """
        email = (u.get("email") or "").lower()
        name = (u.get("name") or "").lower()
        if not name and not email:
            return True
        if "test" in email or "example.com" in email or "+ci" in email:
            return True
        if name.startswith("new") or "test" in name:
            return True
        return False

    for user in users:
        # Ignora contatos de teste/seed para não poluir a UI (apenas para chamadas HTTP)
        if exclude_seeds and is_seed_user(user):
            continue
        user_id = str(user["_id"])

        user_id = str(user["_id"])
        
        # Busca última mensagem (com ou sem contactId)
        last_msg = await db.messages.find_one(
            {"$or": [{"contactId": user_id}, {"userId": user_id}]},
            sort=[("createdAt", -1)]
        )
        
        contact = Contact(
            id=user_id,
            name=user.get("name", user["email"]),
            email=user.get("email"),
            avatar=user.get("avatar"),
            lastMessage=last_msg.get("text", "") if last_msg else "",
            lastMessageTime=int(last_msg["createdAt"].timestamp() * 1000) if last_msg else 0,
            unreadCount=0,
            online=False
        )
        contacts.append(contact)

    # Inclui contatos externos criados pelo usuário
    try:
        external_contacts = await db.contacts.find({"createdBy": current_user_id}).to_list(None)
        for ec in external_contacts:
            # Aplica mesma heurística para evitar contatos de teste externos (apenas para chamadas HTTP)
            ec_name = (ec.get("name") or "").lower()
            ec_email = (ec.get("email") or "").lower()
            if exclude_seeds and ("test" in ec_email or "example.com" in ec_email or ec_name.startswith("new") or "test" in ec_name):
                continue

            ec_id = str(ec.get("_id"))
            last_msg = await db.messages.find_one({"contactId": ec_id}, sort=[("createdAt", -1)])
            contact = Contact(
                id=ec_id,
                name=ec.get("name", ec.get("phone") or ec.get("email") or "Contato"),
                email=ec.get("email"),
                avatar=ec.get("avatar"),
                lastMessage=last_msg.get("text", "") if last_msg else "",
                lastMessageTime=int(last_msg["createdAt"].timestamp() * 1000) if last_msg else 0,
                unreadCount=0,
                online=False
            )
            contacts.append(contact)
    except Exception:
        # Se a coleção não existir ainda, ignora
        pass
    
    # Ordena por última mensagem
    contacts.sort(key=lambda c: c.lastMessageTime or 0, reverse=True)
    
    return contacts


class ConversationResponse(BaseModel):
    messages: List[ConversationMessage]
    hasMore: bool

@router.get("/{contact_id}/messages", response_model=ConversationResponse)
async def get_conversation(
    contact_id: str,
    limit: int = 50,
    before: Optional[int] = None,
    current_user_id: str = Depends(get_current_user_id),
    request: Request = None
):
    # Se chamada via HTTP, 'request' estará presente e devemos exigir header Authorization
    if request is not None:
        if not request.headers.get("Authorization") and not request.headers.get("authorization"):
            raise HTTPException(status_code=401, detail="Token ausente")
    """
    Retorna mensagens de uma conversa específica com um contato
    """
    try:
        # Primeiro tenta buscar em usuários com ObjectId; se não for um ObjectId válido, tenta string
        contact = None
        try:
            contact = await db.users.find_one({"_id": ObjectId(contact_id)})
        except (InvalidId, Exception):
            # tenta buscando por string id (em testes a collection fake pode usar strings)
            try:
                contact = await db.users.find_one({"_id": contact_id})
            except Exception:
                contact = None

        contact_name = None
        # Se não houver usuário com esse id, tenta na coleção de contatos externos (se existir)
        if not contact:
            contact_name = None
            contacts_coll = getattr(db, "contacts", None)
            if contacts_coll is not None:
                try:
                    try:
                        contact_doc = await contacts_coll.find_one({"_id": ObjectId(contact_id)})
                    except InvalidId:
                        contact_doc = await contacts_coll.find_one({"_id": contact_id})
                    if contact_doc:
                        contact_name = contact_doc.get("name", contact_doc.get("email") or contact_doc.get("phone"))
                except Exception:
                    contact_name = None

            # Se não encontrou em nenhum lugar, usa o próprio contact_id como fallback (compatibilidade)
            if not contact_name:
                contact_name = contact_id
        else:
            contact_name = contact.get("name", contact.get("email"))
        
        # Filtro: conversa entre usuário autenticado e contato
        query = {
            "$or": [
                {"userId": current_user_id, "contactId": contact_id},
                {"userId": contact_id, "contactId": current_user_id},
                # Compatibilidade legado: usa author pelo nome do contato, mas limita ao usuário atual
                {"author": contact_name, "userId": current_user_id}
            ]
        }
        
        # Paginação
        if before:
            # 'before' é timestamp em ms
            query["createdAt"] = {"$lt": datetime.fromtimestamp(before / 1000.0)}
            # Alguns registros usam campo 'timestamp' em ms em vez de createdAt
            query["timestamp"] = {"$lt": before}
        
        # Busca mensagens
        cursor = db.messages.find(query).sort("createdAt", -1).limit(limit)
        messages = await cursor.to_list(None)
        messages.reverse()  # Ordem cronológica
        
        # Converte para response model
        result = []
        for msg in messages:
            from storage import presign_get
            
            # Algumas mensagens antigas podem ter 'timestamp' em vez de 'createdAt'
            ts = None
            if "createdAt" in msg and hasattr(msg["createdAt"], "timestamp"):
                ts = int(msg["createdAt"].timestamp() * 1000)
            else:
                ts = int(msg.get("timestamp", 0))

            message_dict = {
                "id": str(msg["_id"]),
                "author": msg.get("author", ""),
                "text": msg.get("text", ""),
                "timestamp": ts,
                "type": msg.get("type", "text"),
                "status": msg.get("status", "sent"),
                "userId": msg.get("userId"),  # 🆕 ID do remetente
                "contactId": msg.get("contactId")  # 🆕 ID do destinatário
            }
            
            # Adiciona attachment se existir
            if "attachment" in msg:
                message_dict["attachment"] = msg["attachment"]
                # Pode ser uma referência por 'key' (para presign) ou já ter 'url'
                if isinstance(msg["attachment"], dict):
                    if "key" in msg["attachment"]:
                        try:
                            message_dict["url"] = presign_get(msg["attachment"]["key"])
                        except Exception:
                            message_dict["url"] = msg["attachment"].get("url")
                    else:
                        message_dict["url"] = msg["attachment"].get("url")
                else:
                    # Caso inesperado, ignora a url
                    message_dict["url"] = None
            
            result.append(ConversationMessage(**message_dict))
        
        return ConversationResponse(
            messages=result,
            hasMore=len(messages) == limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar conversa: {e}")
        raise HTTPException(500, f"Erro ao buscar conversa: {str(e)}")


@router.post("/{contact_id}/mark-read")
@router.put("/{contact_id}/read")
async def mark_conversation_read_put(contact_id: str, current_user_id: str = Depends(get_current_user_id), request: Request = None):
    """Compatibilidade: rota PUT /contacts/{id}/read usada nos testes"""
    # Reaproveita a implementação existente
    return await mark_conversation_read(contact_id, current_user_id, request)


@router.get("/unread-count")
async def unread_counts(current_user_id: str = Depends(get_current_user_id), request: Request = None):
    """Retorna a contagem de conversas e mensagens não-lidas para o usuário autenticado.

    - unreadConversations: número de contatos com pelo menos 1 mensagem não-lida (conversas)
    - unreadMessages: número total de mensagens não-lidas
    """
    # Se chamada via HTTP, exige header Authorization
    if request is not None:
        if not request.headers.get("Authorization") and not request.headers.get("authorization"):
            raise HTTPException(status_code=401, detail="Token ausente")
    try:
        # Filtra mensagens dirigidas ao usuário que não estão marcadas como 'read'
        filter_query = {"contactId": current_user_id, "status": {"$ne": "read"}}

        # Conta total de mensagens não-lidas
        unread_messages = await db.messages.count_documents(filter_query)

        # Conta conversas únicas (distinct userId) que têm mensagens não-lidas
        try:
            distinct_senders = await db.messages.distinct("userId", filter_query)
            # Remove null/None e o id do próprio usuário se presente
            distinct_senders = [s for s in distinct_senders if s]
            unread_conversations = len(distinct_senders)
        except Exception:
            # Fallback: tenta agregar manualmente (mais custoso)
            cursor = db.messages.find(filter_query, {"userId": 1})
            rows = await cursor.to_list(None)
            senders = set(r.get("userId") for r in rows if r.get("userId"))
            unread_conversations = len(senders)

        return {"unreadConversations": unread_conversations, "unreadMessages": unread_messages}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao calcular unread counts: {e}")
        raise HTTPException(500, f"Erro ao calcular unread counts: {str(e)}")async def mark_conversation_read(contact_id: str, current_user_id: str = Depends(get_current_user_id), request: Request = None):
    """
    Marca todas as mensagens de um contato como lidas
    """
    # Se chamada via HTTP, exige header Authorization
    if request is not None:
        if not request.headers.get("Authorization") and not request.headers.get("authorization"):
            raise HTTPException(status_code=401, detail="Token ausente")
    try:
        # Tenta buscar em users (ObjectId ou string)
        contact = None
        contact_name = None
        try:
            contact = await db.users.find_one({"_id": ObjectId(contact_id)})
            contact_name = contact.get("name", contact.get("email")) if contact else None
        except (InvalidId, Exception):
            try:
                contact = await db.users.find_one({"_id": contact_id})
                contact_name = contact.get("name", contact.get("email")) if contact else None
            except Exception:
                contact = None
                contact_name = None

        if not contact_name:
            contacts_coll = getattr(db, "contacts", None)
            if contacts_coll is not None:
                try:
                    try:
                        contact_doc = await contacts_coll.find_one({"_id": ObjectId(contact_id)})
                    except InvalidId:
                        contact_doc = await contacts_coll.find_one({"_id": contact_id})
                    if contact_doc:
                        contact_name = contact_doc.get("name", contact_doc.get("email") or contact_doc.get("phone"))
                except Exception:
                    contact_name = None

        # Se não houve contato encontrado, usa contato como string (compatibilidade)
        if not contact_name:
            contact_name = contact_id

        # Atualiza status de mensagens não lidas do contato
        result = await db.messages.update_many(
            {
                "$or": [
                    {"userId": current_user_id, "contactId": contact_id},
                    {"userId": contact_id, "contactId": current_user_id},
                    {"author": contact_name, "userId": current_user_id}
                ],
                "status": {"$ne": "read"}
            },
            {"$set": {"status": "read"}}
        )
        
        # Emite atualização de unread counts via Socket.IO para o usuário que marcou como lido
        try:
            from socket_handlers import emit_unread_counts_for_user
            await emit_unread_counts_for_user(current_user_id)
            # opcional: também notifica o outro participante
            try:
                await emit_unread_counts_for_user(contact_id)
            except Exception:
                pass
        except Exception:
            pass

        return {"updated": result.modified_count}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao marcar como lido: {e}")
        raise HTTPException(500, f"Erro ao marcar como lido: {str(e)}")
