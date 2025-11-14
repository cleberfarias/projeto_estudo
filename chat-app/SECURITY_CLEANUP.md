# 🔒 Guia de Segurança: Remover API Key do Git

## ⚠️ Situação Atual

Seu arquivo `.env` com a **OPENAI_API_KEY** foi commitado no Git 3 vezes:
- Commit `f28fc24`
- Commit `a690adc`
- Commit `ec381ac`

**A chave está exposta no histórico do Git!**

---

## 🚨 Ações Imediatas (FAÇA AGORA!)

### 1. Revogar a chave atual da OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Faça login
3. Encontre a chave que termina com `...KaSFEA`
4. Clique em **"Delete"** ou **"Revoke"**
5. Confirme a revogação

✅ **Isso impede que qualquer pessoa use sua chave antiga**

---

### 2. Gerar nova chave

1. Na mesma página, clique em **"Create new secret key"**
2. Dê um nome (ex: "Chat App - Local Dev")
3. **Copie a chave** (você não poderá vê-la novamente!)
4. Guarde em um lugar seguro (gerenciador de senhas)

---

### 3. Atualizar .env local

Edite o arquivo `.env` e substitua a chave antiga pela nova:

```env
OPENAI_API_KEY=sk-proj-SUA-NOVA-CHAVE-AQUI
```

**NÃO COMMIT ESTE ARQUIVO!**

---

## 🧹 Limpar Histórico do Git

### Opção 1: Script Automático (Recomendado)

```bash
cd /home/cleber_delgado/workspace/projeto_estudo/chat-app
./cleanup-env-history.sh
```

O script irá:
- Instalar `git-filter-repo` se necessário
- Remover `.env` de todo o histórico
- Preservar todos os outros arquivos e commits

### Opção 2: Manual

```bash
# Instala ferramenta
pip3 install git-filter-repo

# Remove .env do histórico
git filter-repo --path .env --invert-paths --force

# Force push (se necessário)
git push origin --force --all
```

---

## ✅ Verificar Limpeza

Após rodar o script:

```bash
# Verifica se .env ainda aparece no histórico
git log --all --oneline -- .env

# Deve retornar vazio (nenhum resultado)
```

---

## 📋 Commit Final

```bash
# Adiciona .gitignore atualizado
git add .gitignore

# Commit
git commit -m "chore: adiciona .env ao gitignore para prevenir exposição de secrets"

# Push
git push origin TECH-06-Bots-Autmacoes
```

---

## 🔐 Boas Práticas de Segurança

### ✅ Sempre faça:

1. **Nunca** commite arquivos `.env`
2. Use `.env.example` para documentar variáveis necessárias (sem valores reais)
3. Adicione `.env` ao `.gitignore`
4. Use gerenciador de senhas para guardar chaves
5. Configure limites de uso no dashboard da OpenAI
6. Rotacione chaves periodicamente (a cada 3-6 meses)

### ✅ Para produção:

1. Use variáveis de ambiente do sistema operacional
2. Use serviços de gerenciamento de secrets (AWS Secrets Manager, HashiCorp Vault)
3. Configure rate limiting por usuário
4. Monitore custos e uso diariamente
5. Configure alertas de limite de gastos

---

## 🚀 Depois de Limpar

1. **Reinicie o container** para carregar a nova chave:
   ```bash
   docker compose restart api
   ```

2. **Teste o bot de IA**:
   ```
   /ai teste
   @bot olá
   ```

3. **Monitore os logs**:
   ```bash
   docker compose logs -f api
   ```

---

## ❓ Perguntas Frequentes

### Preciso limpar o histórico?

**Sim**, porque:
- A chave antiga está exposta
- Mesmo revogada, é má prática deixar secrets no Git
- Auditorias de segurança podem flaggar isso

### E se já fiz push para o GitHub?

Após limpar o histórico local:

```bash
# Force push para remoto
git push origin --force --all
```

⚠️ **Avisar colaboradores** para re-clonar o repositório!

### A limpeza vai apagar meus commits?

**Não!** O script remove apenas o arquivo `.env`, preservando:
- Todos os outros arquivos
- Todos os commits
- Todo o histórico de mudanças

### Quanto custa se alguém usar minha chave?

**GPT-3.5-turbo:**
- $0.50 por 1 milhão de tokens de entrada
- $1.50 por 1 milhão de tokens de saída
- Uso malicioso pode custar centenas de dólares

**Proteção:** Configure limites na OpenAI!

---

## 📞 Suporte

Se tiver problemas:

1. **Backup primeiro**: `cp -r .git .git.backup`
2. **Tente o script**: `./cleanup-env-history.sh`
3. **Se falhar**: Restaure backup e peça ajuda

---

## ✅ Checklist Final

- [ ] Revogou chave antiga na OpenAI
- [ ] Gerou nova chave
- [ ] Atualizou `.env` local
- [ ] Executou script de limpeza
- [ ] Verificou que `.env` não está no histórico
- [ ] Commitou `.gitignore` atualizado
- [ ] Reiniciou container com nova chave
- [ ] Testou bot de IA
- [ ] Configurou limites de uso na OpenAI

**Tudo certo?** Sua aplicação está segura! 🎉
