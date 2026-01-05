# Configuração Google OAuth - Login de Usuários

Este guia explica como configurar o login com Google (OAuth2) no Chat-IA.

## 📋 Pré-requisitos

- Conta Google Cloud Console
- Projeto Google Cloud ativo
- APIs ativadas no projeto

## 🚀 Configuração Rápida

### 1. Execute o script de configuração

```bash
# Execute FORA do Docker
python3 setup_google_oauth.py
```

O script irá:
- Solicitar seu Google Client ID
- Atualizar o arquivo `.env`
- Fornecer instruções para reiniciar os containers

### 2. Configure no Google Cloud Console

1. **Acesse**: https://console.cloud.google.com/
2. **Selecione** um projeto existente ou crie novo
3. **Ative APIs**:
   - Google Identity API
4. **Credenciais**:
   - Vá em "Credenciais" → "Criar Credenciais" → "ID do cliente OAuth"
   - Tipo: **Aplicativo da Web**
   - Nome: "Chat-IA Login"
5. **URIs autorizadas**:
   - **Origens JavaScript autorizadas**:
     - `http://localhost:5173` (desenvolvimento)
     - `https://seudominio.com` (produção)
   - **URIs de redirecionamento autorizadas**:
     - Não necessário (usamos Google Identity Services)
6. **Copie o Client ID** gerado

### 3. Execute o script

```bash
python3 setup_google_oauth.py
```

Cole o Client ID quando solicitado.

### 4. Reinicie os containers

```bash
docker compose down
docker compose up -d
```

## 🔧 Configuração Manual

Se preferir configurar manualmente:

### 1. Arquivo `.env`

```bash
# Backend
GOOGLE_CLIENT_ID=seu_client_id_aqui.googleusercontent.com

# Frontend
VITE_GOOGLE_CLIENT_ID=seu_client_id_aqui.googleusercontent.com
```

### 2. Reinicie

```bash
docker compose restart
```

## 🧪 Teste

1. **Acesse**: http://localhost:5173/login
2. **Clique**: "Continuar com Google"
3. **Login**: Use sua conta Google
4. **Verifique**: Deve redirecionar para o chat

## 🔒 Segurança

- ✅ **Token verification**: Backend valida tokens com Google
- ✅ **User creation**: Cria usuários automaticamente no primeiro login
- ✅ **JWT tokens**: Mantém compatibilidade com sistema existente
- ✅ **Rate limiting**: Protegido contra abuso

## 📊 Dados do Usuário

O Google OAuth fornece:
- `email`: Email do usuário
- `name`: Nome completo
- `picture`: URL da foto do perfil
- `sub`: ID único do Google

Estes dados são armazenados no MongoDB junto com:
- `auth_provider`: "google"
- `google_id`: ID único do Google
- `created_at`: Data de criação
- `last_login`: Último acesso

## 🐛 Troubleshooting

### Erro: "Google Client ID não configurado"
- Verifique se `VITE_GOOGLE_CLIENT_ID` está definido no `.env`
- Reinicie os containers após alterar variáveis

### Erro: "Token Google inválido"
- Verifique se o Client ID está correto
- Confirme se as APIs estão ativadas no Google Cloud
- Verifique se as origens estão autorizadas

### Erro: "Falha ao carregar Google Identity Services"
- Verifique conexão com internet
- Tente recarregar a página

## 📚 Referências

- [Google Identity Services](https://developers.google.com/identity/gsi/web)
- [OAuth 2.0 Setup](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)

---

**Status**: ✅ Implementado e funcional</content>
<parameter name="filePath">/home/cleber_delgado/workspace/chat-ia/chat-app/docs/GOOGLE_OAUTH_SETUP.md