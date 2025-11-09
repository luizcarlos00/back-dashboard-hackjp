# FeedBreak Backend API 🚀

Backend API for FeedBreak - Educational platform using short videos with personalized E2E (Explain-to-Evaluate) questions.

## 🏗️ Architecture

- **FastAPI** - Modern Python web framework
- **SQLite** - Local database for data persistence
- **Local File Storage** - Audio files stored in the local file system
- **LangChain + GPT-4o-mini** - AI-powered answer analysis

## 📋 Features

### Core Features
- ✅ User management (profile with interests, education level)
- ✅ Video content delivery with progress tracking
- ✅ E2E questions (Explain-to-Evaluate)
- ✅ Text and audio answer submission
- ✅ AI-powered answer analysis with feedback
- ✅ Dashboard with statistics and answer review

### API Endpoints

#### Users
- `POST /api/v1/user` - Create/update user profile
- `GET /api/v1/user/{device_id}` - Get user by device ID

#### Videos
- `GET /api/v1/videos` - List videos (with filters)
- `GET /api/v1/videos/content` - Alias for videos list
- `GET /api/v1/videos/next?device_id=X` - Get next video for user
- `GET /api/v1/videos/{video_id}` - Get specific video

#### Progress
- `POST /api/v1/progress` - Record video completion

#### Questions
- `GET /api/v1/questions?device_id=X&video_id=Y` - Generate E2E question
- `GET /api/v1/questions/prompts` - Get available prompts

#### Answers
- `POST /api/v1/answer` - Submit text answer (with AI analysis)
- `POST /api/v1/answer/audio` - Upload audio answer

#### Dashboard
- `GET /api/v1/dashboard/stats` - Get system statistics
- `GET /api/v1/dashboard/e2e` - Get answers for review

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key

### 1. Setup Environment

Create a `.env` file in the `backend/` directory (see `env.example` for reference):

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here

# Server Configuration (optional)
PORT=8000

# Database URL (optional - defaults to sqlite:///./feedbreak.db)
DATABASE_URL=sqlite:///./feedbreak.db
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Initialize Database

The database will be created automatically on first run, or you can use Alembic migrations:

```bash
# Create initial migration (if needed)
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

### 4. Run Locally

```bash
# Development mode with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or directly
python app/main.py
```

API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 📊 Database Schema

The application uses **SQLite** for local data persistence. The database file (`feedbreak.db`) is created automatically in the backend directory.

### Main Tables

1. **users** - User profiles with nome, email, idade, nivel_educacional
2. **contents** - Content/subject metadata with keywords and difficulty levels
3. **videos** - Educational videos linked to contents
4. **questions** - E2E questions related to contents
5. **answers** - User responses with AI evaluation and scores

The database is managed through SQLAlchemy ORM with Alembic migrations. Models are defined in `app/db_models.py`.

## 🧪 Testing

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Create user
curl -X POST http://localhost:8000/api/v1/user \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-123",
    "nome": "Test User",
    "idade": 25,
    "interesses": ["ciencia", "tecnologia"],
    "nivel_educacional": "superior"
  }'

# Get next video
curl "http://localhost:8000/api/v1/videos/next?device_id=test-device-123"

# Record progress
curl -X POST http://localhost:8000/api/v1/progress \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-123",
    "video_id": "video-uuid-here",
    "completed": true
  }'

# Get question
curl "http://localhost:8000/api/v1/questions?device_id=test-device-123&video_id=video-uuid-here"

# Submit text answer
curl -X POST http://localhost:8000/api/v1/answer \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-123",
    "question_id": "question-uuid-here",
    "video_id": "video-uuid-here",
    "text_response": "Fotossíntese é o processo onde plantas convertem luz solar em energia..."
  }'

# Get dashboard stats
curl http://localhost:8000/api/v1/dashboard/stats
```

## 📝 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Environment configuration
│   ├── database.py                # Database connection
│   ├── db_models.py               # SQLAlchemy models
│   ├── models.py                  # Pydantic models
│   ├── routers/
│   │   ├── users.py               # User endpoints
│   │   ├── contents.py            # Content management
│   │   ├── videos.py              # Video endpoints
│   │   ├── progress.py            # Progress tracking
│   │   ├── questions.py           # E2E questions
│   │   ├── answers.py             # Answer submission
│   │   └── dashboard.py           # Dashboard stats
│   └── services/
│       └── langchain_analyzer.py  # AI answer analysis
├── alembic/                       # Database migrations
├── uploads/
│   └── audio/                     # Uploaded audio files
├── feedbreak.db                   # SQLite database (auto-generated)
├── requirements.txt
└── README.md
```

## 💡 Key Features Explained

### Personalized E2E Questions

After watching N videos (default: 3), users receive an "Explain-to-Evaluate" question:
1. System generates a question based on the video content
2. Question is saved and returned to user

### AI-Powered Answer Analysis

Text answers are analyzed using LangChain + GPT-4o-mini:
1. Evaluates understanding of key concepts
2. Calculates quality score (0.0 - 1.0)
3. Identifies concepts mentioned
4. Generates constructive feedback
5. Determines pass/fail (>= 0.6 = pass)

### Progress Tracking

System tracks:
- Videos watched per user
- When to trigger E2E questions
- View counts per video
- User activity timestamps

## 🔐 Security Notes

**For Production:**
- Set specific CORS origins (not "*")
- Add rate limiting
- Implement proper authentication
- Use environment-specific API keys
- Consider using PostgreSQL or other production databases instead of SQLite
- Implement proper file upload validation and virus scanning
- Set appropriate file size limits

## 📞 Support

For issues or questions:
- Check API docs at `/docs`
- Review application logs
- Test endpoints locally first

## 🎯 Roadmap

Future enhancements:
- [ ] Audio transcription (Whisper API)
- [ ] User authentication (OAuth)
- [ ] Video recommendations engine
- [ ] Analytics dashboard improvements
- [ ] Admin panel for content management

---

**Built for Hackathon** | FastAPI + SQLite + LangChain

