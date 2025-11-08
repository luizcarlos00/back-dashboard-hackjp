from sqlalchemy import Column, String, Integer, Float, Boolean, TIMESTAMP, ARRAY, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class User(Base):
    """
    Tabela de usuários do sistema
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    idade = Column(Integer, nullable=True)
    nivel_educacional = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
    last_active_at = Column(TIMESTAMP)
    
    # Relacionamentos
    answers = relationship("Answer", back_populates="user", cascade="all, delete-orphan")


class Content(Base):
    """
    Tabela de conteúdos/matérias
    Cada conteúdo pode ter vários vídeos e várias questões
    """
    __tablename__ = "contents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    matter = Column(String(100), nullable=True, index=True)
    difficulty_level = Column(Integer, default=1, index=True)  # 1-5
    keywords = Column(ARRAY(Text), default=[])
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    videos = relationship("Video", back_populates="content", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="content", cascade="all, delete-orphan")


class Video(Base):
    """
    Tabela de vídeos relacionados a um conteúdo/matéria
    """
    __tablename__ = "videos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=False)
    
    # Metadados do vídeo
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    content = relationship("Content", back_populates="videos")


class Question(Base):
    """
    Tabela de questões relacionadas a um conteúdo/matéria
    """
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    question_text = Column(Text, nullable=False)
 
    expected_keywords = Column(ARRAY(Text), default=[])
    
    difficulty_level = Column(Integer, default=1, index=True)  # 1-5
    
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    content = relationship("Content", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    """
    Tabela de respostas dos usuários para as questões
    """
    __tablename__ = "answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Resposta do usuário
    text_response = Column(Text, nullable=True)
    
    # Análise da resposta
    ai_evaluation = Column(Text, nullable=True)
    quality_score = Column(Float, nullable=True)  # 0.0 - 1.0
    
    # Resultado
    is_correct = Column(Boolean, nullable=True, index=True)
    feedback = Column(Text, nullable=True)  # Feedback para o usuário
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
