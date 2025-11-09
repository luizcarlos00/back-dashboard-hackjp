from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


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
    created_at: datetime
    last_active_at: Optional[datetime]


class VideoCreate(BaseModel):
    video_id: str  # ID do YouTube (ex: dQw4w9WgXcQ)
    title: Optional[str] = None
    quantity_until_e2e: int = 3
    order_index: int = 0

class VideoResponse(BaseModel):
    id: str
    content_id: str
    video_id: str
    url: Optional[str] = None
    audio_url: Optional[str] = None
    youtube_url: Optional[str] = None
    title: Optional[str]
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    quantity_until_e2e: int
    order_index: int
    created_at: datetime

class ActivityCreate(BaseModel):
    question: str
    order_index: int = 0

class ActivityResponse(BaseModel):
    id: str
    content_id: str
    question: str
    order_index: int
    created_at: datetime

class ContentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    publico_alvo: Optional[str] = None  # fundamental, médio, superior, etc
    category: Optional[str] = None
    is_active: bool = True
    videos: List[VideoCreate] = []
    activities: List[ActivityCreate] = []

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    publico_alvo: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class ContentResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    publico_alvo: Optional[str]
    category: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    videos: List[VideoResponse] = []
    activities: List[ActivityResponse] = []


class VideoProgressCreate(BaseModel):
    device_id: str
    video_id: str
    watched: bool = True

class VideoProgressResponse(BaseModel):
    id: str
    user_id: str
    video_id: str
    watched: bool
    watched_at: datetime


class ActivityResponseCreate(BaseModel):
    device_id: str
    activity_id: str
    answer: str
    grau_aprendizagem: Optional[float] = None
    responded: bool = True

class ActivityResponseUpdate(BaseModel):
    answer: Optional[str] = None
    grau_aprendizagem: Optional[float] = Field(None, ge=0.0, le=1.0)
    responded: Optional[bool] = None

class UserActivityResponseDetail(BaseModel):
    id: str
    user_id: str
    activity_id: str
    answer: Optional[str]
    grau_aprendizagem: Optional[float]
    responded: bool
    created_at: datetime


class NextVideoResponse(BaseModel):
    video: Optional[VideoResponse]
    watched_count: int
    should_trigger_e2e: bool
    next_activity: Optional[ActivityResponse] = None


class DashboardStats(BaseModel):
    total_users: int
    total_videos: int
    total_activities: int
    total_video_watches: int
    total_activity_responses: int
    avg_grau_aprendizagem: Optional[float]
    most_popular_content: Optional[str]

class UserStats(BaseModel):
    user_id: str
    user_nome: str
    videos_watched: int
    activities_completed: int
    avg_grau_aprendizagem: Optional[float]
    last_active: Optional[datetime]
