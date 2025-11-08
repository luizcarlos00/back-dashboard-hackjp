# FeedBreak Backend API 🚀

Backend API for FeedBreak - Educational platform using short videos with personalized E2E (Explain-to-Evaluate) questions.

## 🏗️ Architecture

- **FastAPI** - Modern Python web framework
- **Supabase** - PostgreSQL database + file storage
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
- Supabase account
- OpenAI API key

### 1. Setup Environment

Create a `.env` file in the `backend/` directory:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here

# Server Configuration
PORT=8000
```

### 2. Setup Supabase Database

1. Go to your Supabase project
2. Open SQL Editor
3. Run the schema from `app/database/schema.sql`
4. Create storage bucket:
   - Go to Storage
   - Create bucket named `e2e-audio`
   - Set to private
   - Configure policies as needed

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
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

### Main Tables

1. **users** - User profiles with device_id, nome, idade, interesses, nivel_educacional
2. **videos** - Educational videos with metadata and expected_concepts
3. **user_progress** - Track which videos each user has watched
4. **questions** - E2E questions for user evaluation
5. **answers** - User responses with AI evaluation
6. **e2e_prompts** - Base prompts for question generation

See `app/database/schema.sql` for complete schema.

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
│   ├── models.py                  # Pydantic models
│   ├── routers/
│   │   ├── users.py               # User endpoints
│   │   ├── videos.py              # Video endpoints
│   │   ├── progress.py            # Progress tracking
│   │   ├── questions.py           # E2E questions
│   │   ├── answers.py             # Answer submission
│   │   └── dashboard.py           # Dashboard stats
│   ├── services/
│   │   └── langchain_analyzer.py  # AI answer analysis
│   └── database/
│       └── schema.sql              # Database schema
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
- Secure Supabase RLS policies
- Use environment-specific API keys

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

**Built for Hackathon** | FastAPI + Supabase + LangChain

