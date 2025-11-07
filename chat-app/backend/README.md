# Backend Python - Chat API

Backend do chat em tempo real desenvolvido com **FastAPI**, **Socket.IO**, **MongoDB** e **JWT**.

## 🚀 Stack

- **FastAPI** 0.115.5 - Framework web assíncrono de alta performance
- **python-socketio** 5.11.4 - WebSockets em tempo real
- **Motor** 3.6.0 - Driver MongoDB assíncrono
- **Pydantic** 2.10.2 - Validação de dados com type hints
- **PyJWT** 2.10.1 - Autenticação com JSON Web Tokens
- **Passlib + bcrypt** - Hashing seguro de senhas
- **Uvicorn** 0.32.1 - Servidor ASGI

## 📁 Estrutura

```
backend/
├── main.py           # FastAPI app + Socket.IO handlers
├── models.py         # Modelos Pydantic (validação)
├── database.py       # Conexão MongoDB com Motor
├── auth.py           # JWT: create_token, decode_token, hash_password
├── users.py          # Rotas de autenticação (registro/login)
├── requirements.txt  # Dependências Python
├── Dockerfile        # Build da imagem
└── prisma/
    └── schema.prisma # Schema legado (não usado)
```

## 📡 Endpoints REST

### Health Check
- `GET /` - Verifica se API está rodando

### Autenticação
- `POST /register` - Cria nova conta
  - Body: `{username: string, password: string}`
  - Retorna: `{access_token, token_type, user}`
- `POST /login` - Autentica usuário
  - Body: `{username: string, password: string}`
  - Retorna: `{access_token, token_type, user}`

### Mensagens
- `GET /messages?before=<timestamp>&limit=30` - Histórico paginado
  - Query params:
    - `before` (opcional): Timestamp para paginação
    - `limit` (padrão: 30): Máximo de mensagens
  - Requer: Header `Authorization: Bearer <token>`

## 🔌 Eventos Socket.IO

### Cliente → Servidor
- `chat:send` - Envia mensagem
  - Payload: `{author, text, tempId?, status?, type?}`
  - Requer autenticação via token JWT
- `chat:typing` - Indica que está digitando
  - Payload: `{userId, author, chatId, isTyping}`
- `chat:read` - Marca mensagens como lidas
  - Payload: `{messageIds: string[]}`

### Servidor → Cliente(s)
- `chat:new-message` - Broadcasting de nova mensagem
  - Payload: `{id, author, text, timestamp, status, type}`
- `chat:ack` - Confirma recebimento (Optimistic UI)
  - Payload: `{tempId, id, timestamp}`
- `chat:typing` - Broadcasting de status de digitação
  - Payload: `{userId, author, chatId, isTyping}`
- `chat:delivered` - Mensagem entregue
  - Payload: `{messageId}`
- `chat:read` - Mensagens foram lidas
  - Payload: `{messageIds: string[]}`
- `error` - Notificação de erro
  - Payload: `{message: string}`

## 🛠️ Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar servidor com hot-reload
uvicorn main:socket_app --reload --port 3000

# Ou usar Docker Compose (recomendado)
docker-compose up backend
```

## 🐳 Docker

```bash
# Build da imagem
docker build -t chat-api-python .

# Run standalone
docker run -p 3000:3000 \
  -e DATABASE_URL=mongodb://mongo:27017/chatdb?replicaSet=rs0 \
  -e JWT_SECRET=seu-secret-aqui \
  chat-api-python
```

## 🔐 Variáveis de Ambiente

```env
# MongoDB
DATABASE_URL=mongodb://mongo:27017/chatdb?replicaSet=rs0

# JWT
JWT_SECRET=GERE_UM_SECRET_FORTE_AQUI_64_CHARS_MINIMO
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=43200  # 30 dias
```

## 🔄 Migração Node.js → Python

### Por que Python?

- ✅ FastAPI é extremamente rápido (comparable com Node.js)
- ✅ Assíncrono nativo com `async/await` mais limpo
- ✅ Validação automática com Pydantic (type hints)
- ✅ Documentação interativa automática (Swagger UI)
- ✅ Motor é mais simples que Prisma para MongoDB
- ✅ Python é mais comum em projetos de IA/ML

### Comparação

| Aspecto | Node.js (anterior) | Python (atual) |
|---------|-------------------|----------------|
| Framework | Express + Socket.IO | FastAPI + python-socketio |
| Database | Prisma ORM | Motor (driver nativo async) |
| Validação | Zod | Pydantic (type hints) |
| Auth | JWT manual | PyJWT + Passlib/bcrypt |
| Runtime | tsx/ts-node-dev | uvicorn --reload |
| Tipagem | TypeScript | Python type hints |
| Async | Promises/async-await | async/await nativo |
| Build | tsc → dist/ | Nenhum (interpretado) |
| Performance | Muito rápido | Muito rápido (Starlette) |

### Desafios da Migração

1. **Socket.IO syntax:** `io.emit()` → `await sio.emit()` (tudo é async)
2. **ObjectId:** Conversão `str(doc["_id"])` para enviar ao frontend
3. **Timestamps:** `Date.now()` → `datetime.utcnow()` → `.timestamp() * 1000`
4. **Environment:** `process.env.VAR` → `os.getenv("VAR")`
5. **Imports:** Sem hot-reload de imports (precisa reiniciar em alguns casos)

## 📚 Features Implementadas

### ✅ TECH-02: Persistência MongoDB
- Motor async driver
- Collection `messages` com histórico
- Paginação com cursor (`before` timestamp)

### ✅ TECH-03: Autenticação JWT
- Registro e login com validação Pydantic
- Hashing bcrypt para senhas
- Token JWT com expiração de 30 dias
- Socket.IO protegido (requer token no `auth`)

### ✅ TECH-04: Eventos UX Avançados
- `chat:ack` para Optimistic UI
- `chat:typing` com broadcast
- `chat:delivered` e `chat:read` para status
- Session tracking com `environ["user_id"]`

## 📖 Documentação da API

Com o servidor rodando, acesse:

- **Swagger UI:** http://localhost:3000/docs
- **ReDoc:** http://localhost:3000/redoc

FastAPI gera documentação interativa automaticamente! 🎉

## 🧪 Testando

```bash
# Health check
curl http://localhost:3000/

# Registro
curl -X POST http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","password":"123456"}'

# Login
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","password":"123456"}'

# Mensagens (com token)
curl http://localhost:3000/messages?limit=10 \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```
