# Back Dashboard HackJP

Backend API for FeedBreak - Educational platform using short videos with personalized E2E (Explain-to-Evaluate) questions.

## Tech Stack
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **LangChain + GPT-4o-mini** - AI-powered answer analysis

## Quick Start

### 🐳 Usando Docker (Recomendado)

```bash
# 1. Configure variáveis de ambiente
cd backend
cp env.docker.example .env
# Edite .env e adicione sua OPENAI_API_KEY

# 2. Iniciar com Docker
cd ..
docker-compose up --build

# Pronto! API rodando em http://localhost:8000
```

### 💻 Sem Docker

```bash
# Setup
cd backend
pip install -r requirements.txt

# Configure .env file
cp env.example .env  # Edit with your credentials

# Initialize database
python init_db.py

# Run server
uvicorn app.main:app --reload
```

## Documentation
- API Docs: http://localhost:8000/docs
- Docker Guide: [README_DOCKER.md](README_DOCKER.md)
- See `backend/README.md` for detailed documentation