"""Módulo de integração com ChatGPT/OpenAI."""

import os
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Contexto do bot
SYSTEM_PROMPT = """Você é um assistente de chat inteligente e amigável.
Responda de forma concisa e útil.
Se não souber algo, seja honesto.
Mantenha um tom profissional mas descontraído."""


async def ask_chatgpt(message: str, conversation_history: Optional[list] = None) -> str:
    """
    Envia uma mensagem para o ChatGPT e retorna a resposta.
    
    Args:
        message: Mensagem do usuário
        conversation_history: Histórico de conversa (opcional)
        
    Returns:
        Resposta do ChatGPT
    """
    if not OPENAI_API_KEY:
        return "❌ Bot de IA não configurado. Configure OPENAI_API_KEY nas variáveis de ambiente."
    
    # Prepara as mensagens
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Adiciona histórico se fornecido (últimas 5 mensagens para não estourar tokens)
    if conversation_history:
        messages.extend(conversation_history[-5:])
    
    # Adiciona mensagem atual
    messages.append({"role": "user", "content": message})
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENAI_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            
            if response.status_code != 200:
                error_msg = response.json().get("error", {}).get("message", "Erro desconhecido")
                return f"❌ Erro na API OpenAI: {error_msg}"
            
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
            
    except httpx.TimeoutException:
        return "⏱️ Timeout ao conectar com ChatGPT. Tente novamente."
    except Exception as e:
        return f"❌ Erro ao processar resposta: {str(e)}"


def is_ai_question(text: str) -> bool:
    """
    Verifica se a mensagem é uma pergunta para o bot de IA.
    
    Detecta padrões como:
    - @bot <pergunta>
    - bot, <pergunta>
    - Mensagens com "?" direcionadas ao bot
    
    Args:
        text: Texto da mensagem
        
    Returns:
        True se for uma pergunta para o bot
    """
    text_lower = text.lower().strip()
    
    # Padrões que indicam uma pergunta ao bot
    triggers = [
        text_lower.startswith("@bot"),
        text_lower.startswith("bot,"),
        text_lower.startswith("hey bot"),
        text_lower.startswith("ei bot"),
    ]
    
    return any(triggers)


def clean_bot_mention(text: str) -> str:
    """
    Remove menções ao bot do texto.
    
    Args:
        text: Texto original
        
    Returns:
        Texto limpo sem menções
    """
    text = text.strip()
    
    # Remove prefixos comuns
    prefixes = ["@bot", "bot,", "hey bot", "ei bot", "bot"]
    
    for prefix in prefixes:
        if text.lower().startswith(prefix):
            text = text[len(prefix):].strip()
            # Remove vírgula ou dois pontos após o prefixo
            if text.startswith((",", ":")):
                text = text[1:].strip()
            break
    
    return text
