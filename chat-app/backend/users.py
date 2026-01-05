from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from datetime import datetime
from database import db
from auth import hash_password, verify_password, create_access_token
from middleware.rate_limit import check_rate_limit, login_limiter, register_limiter
import os
import secrets
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


router = APIRouter(prefix="/auth", tags=["auth"])
users = db.users


class RegisterIn(BaseModel):
    email: EmailStr
    name: str
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(data: RegisterIn, request: Request):
    """Registra novo usuário"""
    # Rate limiting: 3 registros por hora por IP
    check_rate_limit(request, register_limiter)
    
    if await users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    doc = {
        "email": data.email,
        "name": data.name,
        "password": hash_password(data.password),
        "role": "user",
        "created_at": datetime.utcnow()
    }
    
    await users.insert_one(doc)
    return {"message": "Usuário registrado com sucesso"}


@router.post("/login")
async def login(data: LoginIn, request: Request):
    """Autentica usuário e retorna token JWT"""
    # Rate limiting: 5 tentativas por 5 minutos por IP
    check_rate_limit(request, login_limiter)
    
    user = await users.find_one({"email": data.email})
    
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_access_token(str(user["_id"]))

    # Retorna token e dados do usuário (compatível com frontend)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user.get("name", "")
        }
    }
    
class GoogleAuthIn(BaseModel):
    token: str  # Google ID Token


@router.post("/google")
async def google_auth(data: GoogleAuthIn, request: Request):
    """Autentica usuário via Google OAuth"""
    try:
        # Verifica o token com Google
        idinfo = id_token.verify_oauth2_token(
            data.token,
            google_requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )

        # Extrai informações do usuário
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', email.split('@')[0])
        picture = idinfo.get('picture', '')

        # Verifica se usuário já existe
        user = await users.find_one({"$or": [{"email": email}, {"google_id": google_id}]})

        if not user:
            # Cria novo usuário
            user_doc = {
                "email": email,
                "name": name,
                "google_id": google_id,
                "picture": picture,
                "auth_provider": "google",
                "role": "user",
                "created_at": datetime.utcnow(),
                "last_login": datetime.utcnow()
            }
            result = await users.insert_one(user_doc)
            user_id = result.inserted_id
        else:
            # Atualiza último login
            user_id = user["_id"]
            await users.update_one(
                {"_id": user_id},
                {"$set": {"last_login": datetime.utcnow()}}
            )

        # Gera token JWT
        token = create_access_token(str(user_id))

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user_id),
                "email": email,
                "name": name,
                "picture": picture,
                "auth_provider": "google"
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail="Token Google inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na autenticação Google: {str(e)}")  