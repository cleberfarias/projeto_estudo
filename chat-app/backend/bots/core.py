"""Módulo core para processamento de comandos de bots."""

from .commands import COMMANDS


def is_command(text: str) -> bool:
    """Verifica se o texto é um comando (começa com /)."""
    return text.strip().startswith("/")


def parse_command(text: str) -> tuple[str, list[str]]:
    """
    Parseia um comando extraindo nome e argumentos.
    
    Args:
        text: Texto do comando (ex: "/echo hello world")
        
    Returns:
        Tupla (nome_do_comando, lista_de_argumentos)
    """
    parts = text.strip()[1:].split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def run_command(text: str) -> str | None:
    """
    Executa um comando e retorna a resposta.
    
    Args:
        text: Texto do comando completo
        
    Returns:
        Resposta do comando ou mensagem de erro
    """
    if not text or not is_command(text):
        return None
        
    name, args = parse_command(text)
    fn = COMMANDS.get(name)
    if not fn:
        return "Comando não reconhecido. Use /help"
    return fn(args)