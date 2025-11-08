# FeedBreak API Reference 📚

Quick reference for all API endpoints with request/response examples.

**Base URL (Local):** `http://localhost:8000`

All API endpoints are prefixed with `/api/v1`

---

## 🔍 Health & Info

### GET /health
Check if API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "FeedBreak API is running",
  "version": "1.0.0"
}
```

---

## 👤 Users

### POST /api/v1/user
Create or update user profile (upsert based on device_id).

**Request Body:**
```json
{
  "device_id": "android-device-123",
  "nome": "Maria Silva",
  "idade": 17,
  "interesses": ["ciência", "tecnologia", "matemática"],
  "nivel_educacional": "ensino_medio"
}
```

**Response (200):**
```json
{
  "id": "uuid-here",
  "device_id": "android-device-123",
  "nome": "Maria Silva",
  "idade": 17,
  "interesses": ["ciência", "tecnologia", "matemática"],
  "nivel_educacional": "ensino_medio",
  "videos_until_e2e": 3,
  "created_at": "2025-11-08T10:00:00",
  "last_active_at": "2025-11-08T10:00:00"
}
```

### GET /api/v1/user/{device_id}
Get user profile by device ID.

**Response (200):** Same as POST response  
**Response (404):** `{"detail": "User not found"}`

---

## 🎥 Videos

### GET /api/v1/videos
List available videos with filters and pagination.

**Query Parameters:**
- `category` (optional): Filter by category
- `limit` (optional, default: 20): Number of results
- `offset` (optional, default: 0): Pagination offset

**Example:** `/api/v1/videos?category=ciencias&limit=10&offset=0`

**Response (200):**
```json
{
  "videos": [
    {
      "id": "uuid",
      "title": "Como Funciona a Fotossíntese",
      "description": "Explicação sobre fotossíntese...",
      "url": "https://youtube.com/...",
      "thumbnail_url": "https://img.youtube.com/...",
      "duration_seconds": 180,
      "category": "ciencias",
      "difficulty": 1,
      "keywords": ["biologia", "plantas"],
      "expected_concepts": ["luz solar", "clorofila", "energia"],
      "view_count": 42,
      "created_at": "2025-11-08T10:00:00"
    }
  ],
  "total": 15,
  "limit": 10,
  "offset": 0
}
```

### GET /api/v1/videos/content
Alias for `/videos` - same functionality.

### GET /api/v1/videos/next
Get next video for user to watch (personalized).

**Query Parameters:**
- `device_id` (required): User's device ID

**Example:** `/api/v1/videos/next?device_id=android-device-123`

**Response (200):**
```json
{
  "video": {
    "id": "uuid",
    "title": "Como Funciona a Fotossíntese",
    "description": "...",
    "url": "https://youtube.com/...",
    "thumbnail_url": "https://img.youtube.com/...",
    "duration_seconds": 180,
    "category": "ciencias",
    "difficulty": 1,
    "keywords": ["biologia"],
    "expected_concepts": ["luz solar", "clorofila"],
    "view_count": 42,
    "created_at": "2025-11-08T10:00:00"
  },
  "watched_count": 2,
  "should_trigger_e2e": false
}
```

**Note:** `should_trigger_e2e` will be `true` when user should answer a question after this video.

### GET /api/v1/videos/{video_id}
Get specific video by ID.

**Response (200):** Single video object  
**Response (404):** `{"detail": "Video not found"}`

---

## 📊 Progress

### POST /api/v1/progress
Record that user watched a video.

**Request Body:**
```json
{
  "device_id": "android-device-123",
  "video_id": "uuid-of-video",
  "completed": true
}
```

**Response (200):**
```json
{
  "success": true,
  "watched_count": 3,
  "should_trigger_e2e": true
}
```

**Note:** If `should_trigger_e2e` is `true`, show E2E question screen to user.

**Response (404):** `{"detail": "User not found"}` or `{"detail": "Video not found"}`

---

## ❓ Questions (E2E)

### GET /api/v1/questions
Generate personalized E2E question for user.

**Query Parameters:**
- `device_id` (required): User's device ID
- `video_id` (required): Video that was watched

**Example:** `/api/v1/questions?device_id=android-device-123&video_id=uuid`

**Response (200):**
```json
{
  "id": "question-uuid",
  "user_id": "user-uuid",
  "video_id": "video-uuid",
  "question_text": "Explique com suas próprias palavras como funciona a fotossíntese e qual sua importância para a vida na Terra.",
  "created_at": "2025-11-08T10:05:00"
}
```

**Note:** Question is personalized based on user's profile (age, interests, education level).

### GET /api/v1/questions/prompts
Get list of available base prompts (reference only).

**Response (200):**
```json
{
  "prompts": [
    {
      "id": "uuid",
      "text": "Explique o conceito que você acabou de aprender...",
      "category": "geral",
      "created_at": "2025-11-08T10:00:00"
    }
  ]
}
```

---

## 💬 Answers

### POST /api/v1/answer
Submit text answer to E2E question (with AI analysis).

**Request Body:**
```json
{
  "device_id": "android-device-123",
  "question_id": "question-uuid",
  "video_id": "video-uuid",
  "text_response": "Fotossíntese é o processo onde plantas convertem luz solar em energia usando clorofila. A planta absorve CO2 e água, produzindo glicose e oxigênio..."
}
```

**Response (200):**
```json
{
  "id": "answer-uuid",
  "status": "analyzed",
  "quality_score": 0.85,
  "passed": true,
  "ai_evaluation": "Excelente! Você mencionou os conceitos principais: luz solar, clorofila, energia, CO2, água, glicose e oxigênio. Sua explicação demonstra uma boa compreensão do processo de fotossíntese.",
  "concepts_identified": ["luz solar", "clorofila", "energia", "CO2", "água", "glicose", "oxigênio"],
  "missing_concepts": [],
  "audio_url": null
}
```

**Quality Score Scale:**
- `0.0-0.4`: Poor understanding
- `0.5-0.6`: Basic understanding (incomplete)
- `0.7-0.8`: Good understanding
- `0.9-1.0`: Excellent understanding

**Passed:** `true` if `quality_score >= 0.6`

### POST /api/v1/answer/audio
Submit audio answer to E2E question.

**Request (multipart/form-data):**
- `device_id`: string
- `question_id`: string (UUID)
- `video_id`: string (UUID)
- `file`: audio file (MP3, M4A, WAV)

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/v1/answer/audio \
  -F "device_id=android-device-123" \
  -F "question_id=question-uuid" \
  -F "video_id=video-uuid" \
  -F "file=@/path/to/audio.mp3"
```

**Response (200):**
```json
{
  "id": "answer-uuid",
  "status": "saved",
  "audio_url": "https://storage.supabase.com/e2e-audio/...",
  "quality_score": null,
  "passed": null,
  "ai_evaluation": "Áudio salvo com sucesso. Análise automática requer transcrição (recurso futuro).",
  "concepts_identified": null,
  "missing_concepts": null
}
```

**Note:** Audio transcription and analysis are optional future features.

---

## 📈 Dashboard (Admin)

### GET /api/v1/dashboard/stats
Get system statistics.

**Response (200):**
```json
{
  "total_users": 156,
  "total_videos_watched": 1250,
  "total_answers": 285,
  "answers_audio_count": 120,
  "answers_text_count": 165,
  "avg_quality_score": 0.78,
  "pass_rate": 0.82,
  "top_categories": [
    {"category": "ciencias", "count": 450},
    {"category": "tecnologia", "count": 320},
    {"category": "matematica", "count": 280}
  ]
}
```

### GET /api/v1/dashboard/e2e
Get list of answers for review.

**Query Parameters:**
- `response_type` (optional): Filter by "audio" or "text"
- `passed` (optional): Filter by `true` or `false`
- `limit` (optional, default: 50): Number of results

**Example:** `/api/v1/dashboard/e2e?response_type=text&passed=true&limit=20`

**Response (200):**
```json
{
  "responses": [
    {
      "id": "answer-uuid",
      "user_id": "user-uuid",
      "user_nome": "Maria Silva",
      "video_title": "Como Funciona a Fotossíntese",
      "question_text": "Explique com suas próprias palavras...",
      "response_type": "text",
      "text_response": "Fotossíntese é...",
      "audio_url": null,
      "transcription": null,
      "ai_evaluation": "Excelente! Você mencionou...",
      "quality_score": 0.85,
      "passed": true,
      "concepts_identified": ["luz solar", "clorofila", "energia"],
      "created_at": "2025-11-08T10:15:00"
    }
  ],
  "total": 1,
  "limit": 20
}
```

---

## 🔐 Error Responses

All endpoints may return these error codes:

### 400 Bad Request
```json
{
  "detail": "Invalid request format or parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 📝 Common Flows

### 1. User First Time Setup
```
1. POST /api/v1/user (create user)
2. GET /api/v1/videos (browse videos)
```

### 2. Watch Video Flow
```
1. GET /api/v1/videos/next?device_id=X (get next video)
2. User watches video
3. POST /api/v1/progress (record completion)
4. Check response.should_trigger_e2e
```

### 3. E2E Question Flow
```
1. GET /api/v1/questions?device_id=X&video_id=Y (get question)
2. User answers (text or audio)
3. POST /api/v1/answer (submit text answer with analysis)
   OR
   POST /api/v1/answer/audio (upload audio)
4. Show feedback to user
```

### 4. Admin Dashboard
```
1. GET /api/v1/dashboard/stats (overview)
2. GET /api/v1/dashboard/e2e (review answers)
```

---

## 🌐 Categories

Available video categories:
- `ciencias` - Science
- `tecnologia` - Technology
- `matematica` - Math
- `historia` - History
- `portugues` - Portuguese/Language
- `geografia` - Geography

## 📚 Education Levels

Possible values for `nivel_educacional`:
- `fundamental` - Elementary School
- `ensino_medio` - High School
- `superior` - College/University
- `pos_graduacao` - Post-Graduate
- `unknown` - Not specified

---

## 🧪 Testing

Use the provided `test_api.py` script:

```bash
# Start server first
python app/main.py

# In another terminal
python test_api.py
```

Or use the interactive API docs at: `http://localhost:8000/docs`

---

## 📞 Support

- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

For issues, check server logs or API response error messages.

