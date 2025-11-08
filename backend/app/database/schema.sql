-- FeedBreak Backend Database Schema
-- Execute this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    idade INT NOT NULL,
    interesses TEXT[] DEFAULT '{}',
    nivel_educacional VARCHAR(100) NOT NULL,
    videos_until_e2e INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP
);

CREATE INDEX idx_users_device_id ON users(device_id);
CREATE INDEX idx_users_last_active ON users(last_active_at);

-- 2. Videos Table
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    thumbnail_url TEXT,
    duration_seconds INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    difficulty INT DEFAULT 1,
    keywords TEXT[] DEFAULT '{}',
    expected_concepts TEXT[] DEFAULT '{}',
    view_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_videos_category ON videos(category);
CREATE INDEX idx_videos_active ON videos(is_active);
CREATE INDEX idx_videos_difficulty ON videos(difficulty);

-- 3. User Progress Table
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    watched_at TIMESTAMP DEFAULT NOW(),
    completed BOOLEAN DEFAULT true
);

CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_video ON user_progress(video_id);
CREATE INDEX idx_progress_watched_at ON user_progress(watched_at);

-- 4. Questions Table
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    generated_by VARCHAR(20) DEFAULT 'n8n' CHECK (generated_by IN ('n8n', 'manual')),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_user ON questions(user_id);
CREATE INDEX idx_questions_video ON questions(video_id);
CREATE INDEX idx_questions_generated_by ON questions(generated_by);

-- 5. Answers Table
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    
    -- Response type and content
    response_type VARCHAR(10) NOT NULL CHECK (response_type IN ('audio', 'text')),
    text_response TEXT,
    audio_url TEXT,
    audio_duration_seconds INT,
    
    -- AI Analysis
    transcription TEXT,
    ai_evaluation TEXT,
    concepts_identified TEXT[] DEFAULT '{}',
    quality_score FLOAT,
    passed BOOLEAN,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_answers_user ON answers(user_id);
CREATE INDEX idx_answers_question ON answers(question_id);
CREATE INDEX idx_answers_video ON answers(video_id);
CREATE INDEX idx_answers_type ON answers(response_type);
CREATE INDEX idx_answers_passed ON answers(passed);
CREATE INDEX idx_answers_created_at ON answers(created_at);

-- 6. E2E Prompts Table (Base prompts for question generation)
CREATE TABLE e2e_prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    text TEXT NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_prompts_category ON e2e_prompts(category);

-- Create Storage Bucket for Audio Files (Run this separately in Supabase Dashboard > Storage)
-- Bucket name: e2e-audio
-- Public: false
-- File size limit: 10MB
-- Allowed MIME types: audio/mpeg, audio/mp4, audio/wav, audio/x-m4a

-- Insert some default E2E prompts
INSERT INTO e2e_prompts (text, category) VALUES
    ('Explique o conceito que você acabou de aprender em 30 segundos, usando suas próprias palavras.', 'geral'),
    ('Descreva uma situação do dia a dia onde você poderia aplicar o que aprendeu neste vídeo.', 'aplicacao'),
    ('Quais são os pontos principais que você entendeu sobre este tema?', 'resumo'),
    ('Como você explicaria este conceito para uma criança de 10 anos?', 'simplificacao');

