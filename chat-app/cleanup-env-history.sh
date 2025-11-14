#!/bin/bash

# Script para remover .env do histórico do Git
# ⚠️ ATENÇÃO: Isso reescreve o histórico do Git!
# Use apenas se tiver certeza e faça backup antes.

echo "🔒 Limpando .env do histórico do Git..."
echo ""
echo "⚠️  ATENÇÃO: Isso irá reescrever o histórico do Git!"
echo "   - Faça backup do repositório antes"
echo "   - Se já fez push para remoto, precisará fazer force push"
echo "   - Outros colaboradores precisarão re-clonar o repositório"
echo ""
read -p "Deseja continuar? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]
then
    echo "❌ Operação cancelada."
    exit 1
fi

# Verifica se git filter-repo está instalado
if ! command -v git-filter-repo &> /dev/null
then
    echo "📦 Instalando git-filter-repo..."
    pip3 install git-filter-repo
fi

# Backup da branch atual
CURRENT_BRANCH=$(git branch --show-current)
echo "📋 Branch atual: $CURRENT_BRANCH"

# Remove .env do histórico
echo "🗑️  Removendo .env do histórico..."
git filter-repo --path .env --invert-paths --force

# Verifica resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ .env removido do histórico com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Revogue a API key antiga: https://platform.openai.com/api-keys"
    echo "   2. Gere uma nova API key"
    echo "   3. Atualize o arquivo .env local com a nova chave"
    echo "   4. Force push (se necessário): git push origin --force --all"
    echo ""
    echo "⚠️  IMPORTANTE: Outros colaboradores precisarão re-clonar o repo!"
else
    echo "❌ Erro ao remover .env do histórico"
    exit 1
fi
