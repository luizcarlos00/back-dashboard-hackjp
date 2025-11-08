# FeedBreak Backend - Setup Guide 🚀

Quick start guide for setting up and running the FeedBreak backend.

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Supabase account created
- [ ] OpenAI API key obtained
- [ ] n8n instance running (or using cloud n8n)

## Step-by-Step Setup

### 1. Supabase Setup

#### A. Create Project
1. Go to https://supabase.com
2. Create new project
3. Wait for database to initialize

#### B. Run Database Schema
1. Open SQL Editor in Supabase dashboard
2. Copy entire content from `app/database/schema.sql`
3. Run the SQL script
4. Verify tables are created

#### C. Create Storage Bucket
1. Go to Storage section
2. Click "Create bucket"
3. Name: `e2e-audio`
4. Make it **private** (not public)
5. Set file size limit: 10MB
6. Allowed MIME types: `audio/mpeg`, `audio/mp4`, `audio/wav`, `audio/x-m4a`

#### D. Get Credentials
1. Go to Settings > API
2. Copy:
   - Project URL (SUPABASE_URL)
   - `anon` `public` key (SUPABASE_KEY)

### 2. OpenAI Setup

1. Go to https://platform.openai.com
2. Navigate to API keys
3. Create new API key
4. Copy the key (starts with `sk-`)
5. **Important**: This key will only be shown once!

### 3. n8n Webhook Setup

#### Option A: Using n8n Cloud
1. Create n8n account at https://n8n.io
2. Create new workflow
3. Add Webhook node (trigger)
4. Add OpenAI node
5. Configure OpenAI node:
   ```
   Prompt: Generate a personalized E2E question for a student based on:
   - Student name: {{$json["user"]["nome"]}}
   - Age: {{$json["user"]["idade"]}}
   - Interests: {{$json["user"]["interesses"]}}
   - Education level: {{$json["user"]["nivel_educacional"]}}
   - Video: {{$json["video"]["title"]}}
   - Expected concepts: {{$json["video"]["expected_concepts"]}}
   
   Generate a thought-provoking question that asks the student to explain
   the concept in their own words, considering their age and interests.
   ```
6. Add Function node to format response:
   ```javascript
   return {
     question: $input.first().json.choices[0].message.content
   };
   ```
7. Activate workflow
8. Copy webhook URL

#### Option B: Self-hosted n8n
1. Install n8n: `npm install -g n8n`
2. Run: `n8n start`
3. Access at http://localhost:5678
4. Follow same steps as Option A

### 4. Backend Environment Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` with your credentials:
   ```bash
   SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   SUPABASE_KEY=eyJhbGc...your-key-here
   OPENAI_API_KEY=sk-...your-key-here
   N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/xxxxx
   PORT=8000
   ```

### 5. Run Locally

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or directly
python app/main.py
```

### 6. Test the API

#### Check Health
```bash
curl http://localhost:8000/health
```

#### View API Docs
Open browser: http://localhost:8000/docs

#### Test User Creation
```bash
curl -X POST http://localhost:8000/api/v1/user \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-123",
    "nome": "João Silva",
    "idade": 18,
    "interesses": ["ciência", "tecnologia"],
    "nivel_educacional": "ensino_medio"
  }'
```

#### Add Test Video (via Supabase SQL Editor)
```sql
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts)
VALUES (
    'Como Funciona a Fotossíntese',
    'Explicação clara sobre o processo de fotossíntese nas plantas',
    'https://www.youtube.com/watch?v=example',
    'https://img.youtube.com/vi/example/maxresdefault.jpg',
    180,
    'ciencias',
    1,
    ARRAY['biologia', 'plantas', 'natureza'],
    ARRAY['luz solar', 'clorofila', 'glicose', 'energia']
);
```

#### Test Next Video
```bash
curl "http://localhost:8000/api/v1/videos/next?device_id=test-123"
```

### 7. Deploy to Railway

#### Using Railway CLI

```bash
# Install Railway CLI
npm install -g railway

# Login
railway login

# Initialize project (in backend directory)
railway init

# Link to project (if already created)
railway link

# Add environment variables
railway variables set SUPABASE_URL="https://..."
railway variables set SUPABASE_KEY="eyJ..."
railway variables set OPENAI_API_KEY="sk-..."
railway variables set N8N_WEBHOOK_URL="https://..."

# Deploy
railway up
```

#### Using Railway Dashboard

1. Go to https://railway.app
2. Create new project
3. Deploy from GitHub repo
4. Add environment variables in Settings
5. Railway will auto-detect Procfile and deploy

### 8. Post-Deployment

1. Test deployed API:
   ```bash
   curl https://your-app.railway.app/health
   ```

2. Update Android app with production URL

3. Monitor logs in Railway dashboard

## Common Issues

### Issue: "SUPABASE_URL must be set"
**Solution**: Check `.env` file exists and has correct values

### Issue: n8n webhook times out
**Solution**: 
- Verify n8n workflow is activated
- Test webhook URL directly with curl
- Check n8n has OpenAI API key configured

### Issue: "Storage bucket not found"
**Solution**: 
- Create `e2e-audio` bucket in Supabase Storage
- Verify bucket name matches exactly

### Issue: LangChain analysis fails
**Solution**:
- Verify OpenAI API key is valid
- Check you have credits in OpenAI account
- Review logs for specific error

### Issue: Import errors
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. ✅ Add sample videos to database
2. ✅ Test E2E flow end-to-end
3. ✅ Configure n8n for production
4. ✅ Set up monitoring/logging
5. ✅ Deploy to Railway
6. ✅ Connect Android app

## Support

- API Docs: http://localhost:8000/docs
- Supabase Docs: https://supabase.com/docs
- n8n Docs: https://docs.n8n.io
- LangChain Docs: https://python.langchain.com/docs

---

**Ready to go! 🎉** Start the server and visit `/docs` to explore the API.

