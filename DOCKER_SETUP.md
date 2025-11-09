# 🐳 Setup Docker - FeedBreak

Guia completo para rodar o projeto usando Docker com backend e frontend integrados.

---

## 📋 Pré-requisitos

- **Docker** versão 20.10+
- **Docker Compose** versão 2.0+
- Arquivo `.env` configurado na raiz do projeto

---

## 🚀 Quick Start

### 1. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na **raiz do projeto** (não no backend!):

```bash
# Copie o template
cp backend/env.example .env

# Edite e adicione sua OpenAI API Key
nano .env
```

**Conteúdo do `.env`:**
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here

# Server Configuration
PORT=8000

# Database
DATABASE_URL=sqlite:///./feedbreak.db
```

### 2. Subir os Containers

```bash
# Construir e iniciar todos os serviços
docker-compose up --build

# OU rodar em background (recomendado)
docker-compose up -d --build
```

**O que acontece:**
1. 🔨 Build do backend (FastAPI)
2. 🔨 Build do dashboard (Next.js)
3. 🚀 Backend inicia na porta 8000
4. 🚀 Dashboard inicia na porta 3000
5. 🔗 Containers se conectam via rede interna

### 3. Acessar os Serviços

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

---

## 🎯 Arquitetura Docker

```
┌─────────────────────────────────────────┐
│         Docker Network (bridge)         │
│                                         │
│  ┌────────────────┐  ┌──────────────┐  │
│  │   Backend      │  │  Dashboard   │  │
│  │   (FastAPI)    │◄─┤  (Next.js)   │  │
│  │   Port: 8000   │  │  Port: 3000  │  │
│  └────────┬───────┘  └──────────────┘  │
│           │                             │
└───────────┼─────────────────────────────┘
            │
    ┌───────▼────────┐
    │ SQLite DB      │
    │ (Volume)       │
    └────────────────┘
```

---

## 📁 Estrutura dos Dockerfiles

### Backend (`backend/Dockerfile`)
- **Base:** Python 3.11-slim
- **Porta:** 8000
- **Features:**
  - Hot reload habilitado
  - Volume montado para desenvolvimento
  - Health check configurado

### Dashboard (`dashboard/Dockerfile`)
- **Base:** Node 20-alpine
- **Porta:** 3000
- **Features:**
  - Multi-stage build (otimizado)
  - Standalone output do Next.js
  - Usuário non-root (segurança)
  - Health check configurado

---

## 🛠️ Comandos Úteis

### Gerenciamento Básico

```bash
# Iniciar todos os serviços
docker-compose up

# Iniciar em background
docker-compose up -d

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga banco!)
docker-compose down -v

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f dashboard
```

### Build e Rebuild

```bash
# Rebuild tudo do zero (sem cache)
docker-compose build --no-cache

# Rebuild apenas o backend
docker-compose build --no-cache backend

# Rebuild apenas o dashboard
docker-compose build --no-cache dashboard

# Rebuild e restart
docker-compose up -d --build
```

### Debugging

```bash
# Ver containers rodando
docker-compose ps

# Entrar no container do backend
docker-compose exec backend bash

# Entrar no container do dashboard
docker-compose exec dashboard sh

# Ver uso de recursos
docker stats

# Inspecionar network
docker network inspect back-dashboard-hackjp_feedbreak-network
```

### Limpeza

```bash
# Remover containers parados
docker-compose down

# Remover containers, networks, e volumes
docker-compose down -v

# Limpar cache de build do Docker
docker builder prune -a

# Limpar tudo (imagens não usadas, containers, etc)
docker system prune -a
```

---

## 🔧 Troubleshooting

### ❌ Erro: "port is already allocated"

**Problema:** Porta 8000 ou 3000 já está em uso

**Solução:**
```bash
# Ver o que está usando a porta
lsof -i :8000
lsof -i :3000

# Matar processo
kill -9 <PID>

# OU mudar a porta no docker-compose.yml
ports:
  - "8001:8000"  # Muda porta externa para 8001
```

### ❌ Backend não conecta ao banco

**Problema:** Volume do banco não está montado corretamente

**Solução:**
```bash
# Parar containers
docker-compose down

# Remover volumes
docker-compose down -v

# Rebuild e criar banco novo
docker-compose up -d --build

# Inicializar banco (dentro do container)
docker-compose exec backend python init_db.py
```

### ❌ Dashboard não conecta ao backend

**Problema:** Variável `NEXT_PUBLIC_API_URL` incorreta

**Solução:**
```bash
# Verificar configuração no docker-compose.yml
# Deve ser: NEXT_PUBLIC_API_URL=http://backend:8000

# Rebuild dashboard
docker-compose up -d --build dashboard
```

### ❌ Erro: "no space left on device"

**Problema:** Docker está usando muito espaço

**Solução:**
```bash
# Limpar imagens antigas
docker image prune -a

# Limpar volumes não usados
docker volume prune

# Limpar tudo
docker system prune -a --volumes
```

### ❌ Changes não aparecem (Hot Reload não funciona)

**Backend:**
- Volume já está configurado ✅
- Mudanças em Python são detectadas automaticamente

**Dashboard:**
- O Dockerfile de produção NÃO tem hot reload
- Para desenvolvimento, use `npm run dev` localmente

---

## 🔄 Modo Desenvolvimento vs Produção

### Desenvolvimento (Current Setup)

**Backend:**
```yaml
volumes:
  - ./backend:/app  # ✅ Hot reload
command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Dashboard:**
- Multi-stage build otimizado
- Sem hot reload (use local para dev)

### Para Hot Reload no Dashboard

Adicione um `docker-compose.dev.yml`:

```yaml
services:
  dashboard:
    build:
      target: deps  # Parar no stage de deps
    volumes:
      - ./dashboard:/app
      - /app/node_modules
    command: npm run dev
```

Usar com:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## 🌐 Variáveis de Ambiente

### Backend (`.env`)
```bash
OPENAI_API_KEY=sk-...          # Obrigatório
DATABASE_URL=sqlite:///./feedbreak.db
PORT=8000
```

### Dashboard (docker-compose.yml)
```yaml
environment:
  - NODE_ENV=production
  - NEXT_PUBLIC_API_URL=http://backend:8000
  - PORT=3000
```

---

## 📊 Health Checks

Ambos os containers têm health checks configurados:

**Backend:**
- URL: `http://localhost:8000/health`
- Interval: 30s
- Start period: 40s

**Dashboard:**
- Verifica se Node.js responde na porta 3000
- Interval: 30s
- Start period: 40s

**Ver status:**
```bash
docker-compose ps
```

---

## 🚀 Deploy em Produção

### Checklist

- [ ] Remove `--reload` do comando do uvicorn
- [ ] Configure `allow_origins` específicas no CORS
- [ ] Use PostgreSQL ao invés de SQLite
- [ ] Configure secrets manager para API keys
- [ ] Habilite HTTPS (nginx reverse proxy)
- [ ] Configure rate limiting
- [ ] Configure logging adequado
- [ ] Use multi-stage build otimizado
- [ ] Configure restart policies adequadas

### Exemplo de Produção

```yaml
services:
  backend:
    image: feedbreak-backend:latest
    command: ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
    restart: always
    
  dashboard:
    image: feedbreak-dashboard:latest
    restart: always
```

---

## 📦 Banco de Dados

### Importante ⚠️

O banco SQLite está sendo **persistido via volume:**

```yaml
volumes:
  - ./backend/feedbreak.db:/app/feedbreak.db
```

**Isso significa:**
- ✅ Dados não são perdidos ao restartar containers
- ✅ Você pode editar o banco localmente
- ⚠️ Não é ideal para produção (use PostgreSQL)

### Inicializar/Resetar Banco

```bash
# Dentro do container
docker-compose exec backend python init_db.py

# Popular com dados de teste
docker-compose exec backend python seed_db.py
```

---

## 🔐 Segurança

### Produção Checklist

1. **Não use root no container** ✅ (Dashboard já configurado)
2. **Não exponha portas desnecessárias**
3. **Use secrets do Docker:**
   ```yaml
   secrets:
     openai_key:
       external: true
   ```
4. **Scan de vulnerabilidades:**
   ```bash
   docker scan feedbreak-backend:latest
   ```
5. **Keep images atualizadas**
6. **Use .dockerignore** ✅ (Já criado)

---

## 📖 Recursos Adicionais

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Next.js Docker Docs](https://nextjs.org/docs/deployment#docker-image)
- [FastAPI Docker Docs](https://fastapi.tiangolo.com/deployment/docker/)

---

## 🎯 Scripts Úteis

Crie um arquivo `scripts.sh` na raiz:

```bash
#!/bin/bash

# Start everything
alias dstart="docker-compose up -d --build"

# Stop everything
alias dstop="docker-compose down"

# View logs
alias dlogs="docker-compose logs -f"

# Rebuild backend
alias drebuild-backend="docker-compose build --no-cache backend && docker-compose up -d backend"

# Rebuild dashboard
alias drebuild-dashboard="docker-compose build --no-cache dashboard && docker-compose up -d dashboard"

# Clean everything
alias dclean="docker-compose down -v && docker system prune -af"
```

Use com: `source scripts.sh`

---

**✅ Pronto!** Seu projeto está completamente dockerizado!

**Próximos passos:**
1. Configure o `.env` com sua OpenAI API Key
2. Rode `docker-compose up -d --build`
3. Acesse http://localhost:3000
4. Comece a desenvolver! 🚀

