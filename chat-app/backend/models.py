from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime
from typing import Optional


class AttachmentInfo(BaseModel):
    """Informações do anexo armazenado no S3/MinIO"""
    bucket: str
    key: str
    filename: str
    mimetype: str


class MessageBase(BaseModel):
    author: str
    text: str
    status: Optional[str] = "sent"
    type: str = "text"  # "text" | "image" | "file"
    attachment: Optional[AttachmentInfo] = None
    contactId: Optional[str] = None  # 🆕 ID do contato da conversa


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: str = Field(alias="_id")
    createdAt: datetime
    model_config = ConfigDict(populate_by_name=True)

    @field_serializer("createdAt")
    def _serialize_created_at(self, v: datetime) -> int:
        return int(v.timestamp() * 1000)


class MessageResponse(BaseModel):
    id: str
    author: str
    text: str
    timestamp: int
    status: str
    type: str
    attachment: Optional[AttachmentInfo] = None
    url: Optional[str] = None  # URL assinada para acesso ao arquivo
