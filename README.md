# 💬 Chat App — Aplicação de Chat em Tempo Real (Vue 3 + FastAPI)

[![Vue 3](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4.8-010101?logo=socket.io)](https://socket.io/)
[![MongoDB](https://img.shields.io/badge/MongoDB-ReplicaSet-47A248?logo=mongodb)](https://www.mongodb.com/)
[![MinIO](https://img.shields.io/badge/Storage-MinIO%20(S3)-FD5E5E?logo=minio)](https://min.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Vuetify](https://img.shields.io/badge/Vuetify-3.10-1867C0?logo=vuetify)](https://vuetifyjs.com/)

> App de chat moderno, com **Vue 3 + Pinia + Vuetify** no front e **FastAPI + python-socketio + MongoDB** no back.  
> Uploads via **MinIO (S3)** e **integração omnichannel** (WhatsApp/Instagram/Facebook).

---

## 🎯 O que este projeto resolve

Este repositório é um projeto de estudo e uma base técnica para construir uma aplicação de chat em tempo real. Em linguagem direta, ele entrega:

- Comunicação em tempo real confiável e escalável com **Socket.IO**, permitindo troca instantânea de mensagens entre cliente e servidor.
- Histórico de conversas persistido no **MongoDB**, com paginação, garantindo que mensagens antigas sejam consultáveis sem travar a interface.
- Upload de arquivos e imagens usando **URLs pré-assinadas** (MinIO/S3), reduzindo carga no backend e permitindo uploads diretos do navegador para o storage.
- Segurança de acesso com **autenticação JWT** e proteção das conexões WebSocket, evitando acessos não autorizados.
- **Integração omnichannel** (WhatsApp Cloud, Instagram, Facebook, WPPConnect), unificando envio/recebimento de mensagens de múltiplos canais.
- **Automação e bots** (APScheduler + comandos) para respostas automáticas, tarefas agendadas e pequenos workflows.
- Sistema de **agentes de IA integrados (OpenAI)** para criar assistentes especializados dentro do chat (suporte, vendas, jurídico, saúde, etc.).
- Ambiente de desenvolvimento pronto para rodar localmente com **Docker Compose**, reduzindo tempo de setup.
- Padrão modular e extensível que serve como base para estudos, prototipação rápida e projetos de produção com ajustes.

Benefícios para desenvolvedores e equipes:

- Economiza tempo ao fornecer uma base pronta com patterns testados (tempo real, presigned uploads, auth, omnichannel).
- Facilita a experimentação com agentes de IA e bots em um ambiente integrado.
- Ajuda a aprender boas práticas (FastAPI assíncrono, Motor, padrões com Socket.IO, presigned URLs, Docker).
- Fornece exemplos claros para evoluções futuras (rooms, notificações push, testes E2E, observabilidade).

---

## 🧭 IA como Core (Assistente Principal)

Este projeto trata a **Inteligência Artificial como peça central** da experiência de atendimento — o Assistente IA é a interface principal para suporte, vendas e operações.

A aplicação vem com agentes pré-configurados (ex.: *Guru, Advogado, Vendedor, Médico, Psicólogo*), mas você pode criar novos bots personalizados com comportamento, prompts e credenciais independentes.

Principais recursos do Assistente IA:

- **Respostas contextuais**: os agentes mantêm parte do contexto da conversa para respostas mais coerentes.
- **Automação de agendamentos, sugestões e ações**: operações automatizadas via agentes (ex.: SDR de auto-agendamento).
- **Multicanal**: agentes podem atuar em canais omnichannel (WhatsApp/Instagram/Facebook) via webhooks/integrações.
- **Extensível**: cada bot pode ter seu próprio prompt e chave OpenAI.

Exemplo de configuração no `.env` / Docker Compose:

```bash
OPENAI_API_KEY="sua-chave-openai"
DEFAULT_AGENT_KEY="guru"          # agente padrão exibido no painel
ASSISTANT_CORE_ENABLED="true"
✨ Recursos

✅ Tempo real com Socket.IO (WebSocket)

✅ Histórico persistido em MongoDB (índice por createdAt + paginação)

✅ Uploads com URL pré-assinada (MinIO/S3)

✅ Autenticação JWT + Socket protegido

✅ UI com Vuetify (dark/light), Pinia e Vue Router

✅ Bots & Automações (APScheduler: cron + keyword)

✅ Omnichannel: WhatsApp Cloud, Instagram Messaging, Facebook Messenger e WPPConnect (dev/homolog)

✅ Docker Compose para subir tudo localmente

## 🏗️ Arquitetura (Visão Geral)

![Arquitetura Core — Cliente ⇄ Servidor ⇄ Dados](./arquitetura-core.png)

> Fluxo principal: Cliente (Vue 3 + Pinia/Vuetify) ⇄ Servidor (FastAPI + Socket.IO) ⇄ Dados (MongoDB + MinIO/S3).
> Mensagens em tempo real via WebSocket, REST para auth/mensagens/uploads e uploads diretos para o storage via URL pré-assinada.


📋 Pré-requisitos

Docker
 e Docker Compose
OU ambiente local com:

Python 3.11+

Node 20+

MongoDB 6+ (com Replica Set ativo se for usar change streams)

🚀 Início Rápido
1) Com Docker (recomendado)
# 1. Clone o repositório
git clone https://github.com/cleberfarias/projeto_estudo.git
cd projeto_estudo/chat-app

# 2. Suba os serviços
docker compose up -d --build

# 3. (Apenas na 1ª vez) Inicie o Replica Set do Mongo
docker compose exec mongo mongosh --eval 'rs.initiate({_id:"rs0",members:[{_id:0,host:"mongo:27017"}]})'


Depois disso:

Frontend disponível em: http://localhost:5173

API/Socket.IO em: http://localhost:8000

MinIO (console): http://localhost:9001
