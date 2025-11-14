from datetime import datetime, timezone
from typing import Callable

def cmd_help(args: list[str]) -> str:
    """Retorna lista de comandos disponíveis."""
    return (
        "🤖 Comandos disponíveis:\n\n"
        "/help - Mostra esta mensagem de ajuda\n"
        "/echo <texto> - Repete o texto fornecido\n"
        "/time - Mostra a hora atual em UTC\n"
        "/ai <pergunta> - Pergunta algo para o ChatGPT\n\n"
        "💡 Dica: Você também pode chamar o bot com @bot <sua pergunta>"
    )

def cmd_echo(args: list[str]) -> str:
    """Repete o texto fornecido."""
    return " ".join(args) if args else "Nada para repetir!"

def cmd_time(args: list[str]) -> str:
    """Retorna a hora atual em UTC."""
    return f"⏰ Agora (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}"


def cmd_ai(args: list[str]) -> str:
    """
    Comando assíncrono placeholder para ChatGPT.
    A lógica real está em main.py pois precisa ser async.
    """
    if not args:
        return "💭 Use: /ai <sua pergunta>\nExemplo: /ai O que é Python?"
    return "🤔 Processando..."  # Será substituído pela resposta real


COMMANDS: dict[str, Callable[[list[str]], str]] = {
    "help": cmd_help,
    "echo": cmd_echo,
    "time": cmd_time,
    "ai": cmd_ai,
}