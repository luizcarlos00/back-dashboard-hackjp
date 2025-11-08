from sqlalchemy import Column, String, Integer, Float, Boolean, TIMESTAMP, ARRAY, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String(255), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    idade = Column(Integer, nullable=False)
    interesses = Column(ARRAY(Text), default=[])
    nivel_educacional = Column(String(100), nullable=False)
    videos_until_e2e = Column(Integer, default=3)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_active_at = Column(TIMESTAMP)
    
    # Relationships
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="user", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="user", cascade="all, delete-orphan")


class Video(Base):
    __tablename__ = "videos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    url = Column(Text, nullable=False)
    thumbnail_url = Column(Text)
    duration_seconds = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(Integer, default=1, index=True)
    keywords = Column(ARRAY(Text), default=[])
    expected_concepts = Column(ARRAY(Text), default=[])
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    progress = relationship("UserProgress", back_populates="video", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="video", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="video", cascade="all, delete-orphan")


class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    watched_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    completed = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    video = relationship("Video", back_populates="progress")


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="questions")
    video = relationship("Video", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Response type and content
    response_type = Column(String(10), nullable=False, index=True)
    text_response = Column(Text)
    audio_url = Column(Text)
    audio_duration_seconds = Column(Integer)
    
    # AI Analysis
    transcription = Column(Text)
    ai_evaluation = Column(Text)
    concepts_identified = Column(ARRAY(Text), default=[])
    quality_score = Column(Float)
    passed = Column(Boolean, index=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    __table_args__ = (
        CheckConstraint("response_type IN ('audio', 'text')", name='check_response_type'),
    )
    
    # Relationships
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    video = relationship("Video", back_populates="answers")


class E2EPrompt(Base):
    __tablename__ = "e2e_prompts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    category = Column(String(50), index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
