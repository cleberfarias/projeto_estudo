#!/usr/bin/env python3
"""
Script para configurar autenticação OAuth2 do Google para login de usuários.
Execute FORA do Docker para configurar as credenciais.
"""

import os
from pathlib import Path

def setup_google_oauth():
    """Configura Google OAuth2 para login de usuários."""

    print("🔐 Configuração Google OAuth2 - Login de Usuários")
    print("=" * 60)
    print()

    print("📋 Passos para obter Google Client ID:")
    print("1. Acesse: https://console.cloud.google.com/")
    print("2. Crie um projeto ou selecione existente")
    print("3. Ative Google Identity API")
    print("4. Vá em 'Credenciais' > 'Criar Credenciais' > 'ID do cliente OAuth'")
    print("5. Tipo: Aplicativo da Web")
    print("6. URIs de redirecionamento autorizadas:")
    print("   - Para desenvolvimento: http://localhost:5173")
    print("   - Para produção: https://seudominio.com")
    print("7. Copie o Client ID")
    print()

    client_id = input("🔑 Cole aqui seu Google Client ID: ").strip()

    if not client_id:
        print("❌ Client ID não pode estar vazio")
        return False

    # Validação básica do formato
    if not client_id.endswith('.googleusercontent.com'):
        print("⚠️  Aviso: O Client ID deve terminar com '.googleusercontent.com'")
        confirm = input("Continuar mesmo assim? (s/N): ").lower().strip()
        if confirm != 's':
            return False

    # Cria arquivo .env se não existir
    env_file = Path('.env')
    if not env_file.exists():
        print("📄 Criando arquivo .env...")
        with open(env_file, 'w') as f:
            f.write("# Arquivo de configuração gerado automaticamente\n\n")

    # Lê conteúdo atual
    with open(env_file, 'r') as f:
        content = f.read()

    # Atualiza ou adiciona variáveis
    lines = content.split('\n')
    updated = False

    for i, line in enumerate(lines):
        if line.startswith('GOOGLE_CLIENT_ID='):
            lines[i] = f'GOOGLE_CLIENT_ID={client_id}'
            updated = True
            break
        elif line.startswith('VITE_GOOGLE_CLIENT_ID='):
            lines[i] = f'VITE_GOOGLE_CLIENT_ID={client_id}'
            updated = True

    if not updated:
        # Adiciona no final se não encontrou
        if not content.endswith('\n'):
            content += '\n'
        content += f'\n# Google OAuth\nGOOGLE_CLIENT_ID={client_id}\nVITE_GOOGLE_CLIENT_ID={client_id}\n'

        with open(env_file, 'w') as f:
            f.write(content)
    else:
        with open(env_file, 'w') as f:
            f.write('\n'.join(lines))

    print("\n✅ Configuração concluída!")
    print(f"📁 Arquivo .env atualizado: {env_file}")
    print(f"🔑 Client ID: {client_id}")
    print()
    print("🐳 Para aplicar as mudanças:")
    print("   docker compose down && docker compose up -d")
    print()
    print("🌐 Teste o login:")
    print("   http://localhost:5173/login")
    print("   → Clique em 'Continuar com Google'")

    return True

if __name__ == "__main__":
    success = setup_google_oauth()
    if not success:
        exit(1)</content>
<parameter name="filePath">/home/cleber_delgado/workspace/chat-ia/chat-app/setup_google_oauth.py