# 🚀 Quick Start - Docker

## 1️⃣ Configure o .env

```bash
# Copie o exemplo
cp backend/env.example .env

# Edite e adicione sua OpenAI API Key
nano .env
```

Adicione:
```
OPENAI_API_KEY=sk-sua_chave_aqui
```

## 2️⃣ Suba os containers

```bash
docker-compose up -d --build
```

## 3️⃣ Acesse

- **Dashboard:** http://localhost:3000
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs

## 🛑 Para parar

```bash
docker-compose down
```

## 📖 Documentação Completa

Veja `DOCKER_SETUP.md` para guia completo!
