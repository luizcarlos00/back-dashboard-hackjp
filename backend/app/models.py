from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# User Models
class UserCreate(BaseModel):
    device_id: str
    nome: str
    idade: int
    interesses: List[str]
    nivel_educacional: str

class UserResponse(BaseModel):
    id: str
    device_id: str
    nome: str
    idade: int
    interesses: List[str]
    nivel_educacional: str
    videos_until_e2e: int
    created_at: datetime
    last_active_at: Optional[datetime]

# Video Models
class VideoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    url: str
    thumbnail_url: Optional[str]
    duration_seconds: int
    category: str
    difficulty: int
    keywords: List[str]
    expected_concepts: List[str]
    view_count: int
    created_at: datetime

class NextVideoResponse(BaseModel):
    video: Optional[VideoResponse]
    watched_count: int
    should_trigger_e2e: bool

# Progress Models
class ProgressRequest(BaseModel):
    device_id: str
    video_id: str
    completed: bool = True

class ProgressResponse(BaseModel):
    success: bool
    watched_count: int
    should_trigger_e2e: bool

# Question Models
class QuestionResponse(BaseModel):
    id: str
    user_id: str
    video_id: str
    question_text: str
    created_at: datetime

# Answer Models
class AnswerTextRequest(BaseModel):
    device_id: str
    question_id: str
    video_id: str
    text_response: str

class AnswerAnalysis(BaseModel):
    quality_score: float = Field(description="Score de 0.0 a 1.0")
    passed: bool = Field(description="Se passou no critério mínimo (>0.6)")
    concepts_identified: List[str] = Field(description="Conceitos mencionados")
    missing_concepts: List[str] = Field(description="Conceitos esperados não mencionados")
    feedback: str = Field(description="Feedback construtivo para o usuário")

class AnswerResponse(BaseModel):
    id: str
    status: str
    quality_score: Optional[float]
    passed: Optional[bool]
    ai_evaluation: Optional[str]
    concepts_identified: Optional[List[str]]
    missing_concepts: Optional[List[str]]
    audio_url: Optional[str]

# Dashboard Models
class DashboardStats(BaseModel):
    total_users: int
    total_videos_watched: int
    total_answers: int
    answers_audio_count: int
    answers_text_count: int
    avg_quality_score: float
    pass_rate: float
    top_categories: List[dict]

class DashboardAnswer(BaseModel):
    id: str
    user_id: str
    user_nome: Optional[str]
    video_title: str
    question_text: str
    response_type: str
    text_response: Optional[str]
    audio_url: Optional[str]
    transcription: Optional[str]
    ai_evaluation: Optional[str]
    quality_score: Optional[float]
    passed: Optional[bool]
    concepts_identified: Optional[List[str]]
    created_at: datetime

