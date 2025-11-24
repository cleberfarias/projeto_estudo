from fastapi import HTTPException, Request
from auth import get_user_id_from_token


def get_current_user_id(request: Request) -> str:
    """Extrai e valida o user_id do token JWT; exige autenticação."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return user_id
