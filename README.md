# Back Dashboard HackJP

Backend API for FeedBreak - Educational platform using short videos with personalized E2E (Explain-to-Evaluate) questions.

## Tech Stack
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **LangChain + GPT-4o-mini** - AI-powered answer analysis

## Quick Start

```bash
# Setup
cd backend
pip install -r requirements.txt

# Configure .env file
cp .env.example .env  # Edit with your credentials

# Initialize database
python init_db.py --drop
python seed_db.py

# Run server
uvicorn app.main:app --reload
```

## Documentation
- API Docs: http://localhost:8000/docs
- See `backend/README.md` for detailed documentation