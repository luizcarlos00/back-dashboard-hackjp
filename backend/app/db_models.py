from sqlalchemy import Column, String, Integer, Float, Boolean, TIMESTAMP, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(255), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    idade = Column(Integer, nullable=True)
    interesses = Column(JSON, default=list)
    nivel_educacional = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
    last_active_at = Column(TIMESTAMP)
    
    video_progress = relationship("UserVideoProgress", back_populates="user", cascade="all, delete-orphan")
    activity_responses = relationship("UserActivityResponse", back_populates="user", cascade="all, delete-orphan")


class Content(Base):
    __tablename__ = "contents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    publico_alvo = Column(String(100), nullable=True, index=True)  # fundamental, médio, superior, etc
    category = Column(String(100), nullable=True, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    videos = relationship("Video", back_populates="content", cascade="all, delete-orphan", order_by="Video.order_index")
    activities = relationship("Activity", back_populates="content", cascade="all, delete-orphan", order_by="Activity.order_index")


class Video(Base):
    __tablename__ = "videos"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content_id = Column(String(36), ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    video_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    quantity_until_e2e = Column(Integer, default=3)
    order_index = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    content = relationship("Content", back_populates="videos")
    user_progress = relationship("UserVideoProgress", back_populates="video", cascade="all, delete-orphan")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content_id = Column(String(36), ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    question = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    content = relationship("Content", back_populates="activities")
    user_responses = relationship("UserActivityResponse", back_populates="activity", cascade="all, delete-orphan")


class UserVideoProgress(Base):
    __tablename__ = "user_video_progress"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id = Column(String(36), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    
    watched = Column(Boolean, default=False)
    watched_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    user = relationship("User", back_populates="video_progress")
    video = relationship("Video", back_populates="user_progress")


class UserActivityResponse(Base):
    __tablename__ = "user_activity_responses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_id = Column(String(36), ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True)
    
    answer = Column(Text, nullable=True)
    grau_aprendizagem = Column(Float, nullable=True)
    responded = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    user = relationship("User", back_populates="activity_responses")
    activity = relationship("Activity", back_populates="user_responses")
