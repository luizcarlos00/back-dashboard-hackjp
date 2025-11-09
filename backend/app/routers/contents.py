"""
Router para gerenciar conteúdos/matérias
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from app.database import get_db
from app.db_models import Content, Video, Question

router = APIRouter()


# Schemas Pydantic
class ContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    difficulty_level: int = Field(default=1, ge=1, le=5)
    keywords: List[str] = Field(default_factory=list)
    is_active: bool = True
    order_index: int = 0


class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    keywords: Optional[List[str]] = None
    is_active: Optional[bool] = None
    order_index: Optional[int] = None


class ContentResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    category: Optional[str]
    difficulty_level: int
    keywords: List[str]
    is_active: bool
    order_index: int
    created_at: datetime
    updated_at: datetime
    video_count: int = 0
    question_count: int = 0

    class Config:
        from_attributes = True


class ContentDetailResponse(ContentResponse):
    videos: List[dict] = []
    questions: List[dict] = []


# Endpoints
@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    """
    Cria um novo conteúdo/matéria
    """
    try:
        new_content = Content(
            title=content.title,
            description=content.description,
            category=content.category,
            difficulty_level=content.difficulty_level,
            keywords=content.keywords,
            is_active=content.is_active,
            order_index=content.order_index
        )
        
        db.add(new_content)
        db.commit()
        db.refresh(new_content)
        
        # Adicionar contagens
        response = ContentResponse.model_validate(new_content)
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conteúdo: {str(e)}"
        )


@router.get("/", response_model=List[ContentResponse])
def list_contents(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    difficulty_level: Optional[int] = Query(None, ge=1, le=5),
    is_active: bool = True,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos os conteúdos com filtros opcionais
    """
    query = db.query(Content)
    
    # Filtros
    if is_active is not None:
        query = query.filter(Content.is_active == is_active)
    
    if category:
        query = query.filter(Content.category == category)
    
    if difficulty_level:
        query = query.filter(Content.difficulty_level == difficulty_level)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Content.title.ilike(search_pattern)) |
            (Content.description.ilike(search_pattern))
        )
    
    # Ordenação e paginação
    query = query.order_by(Content.order_index, desc(Content.created_at))
    contents = query.offset(skip).limit(limit).all()
    
    # Adicionar contagens de vídeos e questões
    result = []
    for content in contents:
        content_dict = ContentResponse.model_validate(content)
        content_dict.video_count = db.query(func.count(Video.id)).filter(Video.content_id == content.id).scalar()
        content_dict.question_count = db.query(func.count(Question.id)).filter(Question.content_id == content.id).scalar()
        result.append(content_dict)
    
    return result


@router.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    """
    Lista todas as categorias únicas de conteúdos
    """
    categories = db.query(Content.category).distinct().filter(
        Content.category.isnot(None),
        Content.is_active == True
    ).all()
    
    return [cat[0] for cat in categories if cat[0]]


@router.get("/{content_id}", response_model=ContentDetailResponse)
def get_content(content_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Busca um conteúdo específico por ID com seus vídeos e questões
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado"
        )
    
    # Buscar vídeos relacionados
    videos = db.query(Video).filter(
        Video.content_id == content_id,
        Video.is_active == True
    ).order_by(Video.order_index).all()
    
    # Buscar questões relacionadas
    questions = db.query(Question).filter(
        Question.content_id == content_id,
        Question.is_active == True
    ).order_by(Question.order_index).all()
    
    # Montar resposta
    response = ContentDetailResponse.model_validate(content)
    response.video_count = len(videos)
    response.question_count = len(questions)
    
    response.videos = [
        {
            "id": str(video.id),
            "title": video.title,
            "description": video.description,
            "url": video.url,
            "thumbnail_url": video.thumbnail_url,
            "duration_seconds": video.duration_seconds,
            "view_count": video.view_count,
            "order_index": video.order_index
        }
        for video in videos
    ]
    
    response.questions = [
        {
            "id": str(question.id),
            "question_text": question.question_text,
            "question_type": question.question_type,
            "difficulty_level": question.difficulty_level,
            "points": question.points,
            "order_index": question.order_index
        }
        for question in questions
    ]
    
    return response


@router.put("/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: uuid.UUID,
    content_update: ContentUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um conteúdo existente
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado"
        )
    
    try:
        # Atualizar apenas os campos fornecidos
        update_data = content_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(content, field, value)
        
        db.commit()
        db.refresh(content)
        
        response = ContentResponse.model_validate(content)
        response.video_count = db.query(func.count(Video.id)).filter(Video.content_id == content.id).scalar()
        response.question_count = db.query(func.count(Question.id)).filter(Question.content_id == content.id).scalar()
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar conteúdo: {str(e)}"
        )


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(content_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Deleta um conteúdo (soft delete - marca como inativo)
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado"
        )
    
    try:
        # Soft delete
        content.is_active = False
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar conteúdo: {str(e)}"
        )


@router.delete("/{content_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
def delete_content_permanent(content_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Deleta permanentemente um conteúdo e todos os seus vídeos e questões
    ⚠️ ATENÇÃO: Esta operação é irreversível!
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado"
        )
    
    try:
        # Deletar permanentemente (cascade vai deletar vídeos e questões)
        db.delete(content)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar conteúdo permanentemente: {str(e)}"
        )


@router.get("/{content_id}/stats")
def get_content_stats(content_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Retorna estatísticas sobre um conteúdo
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado"
        )
    
    # Contar vídeos
    video_count = db.query(func.count(Video.id)).filter(Video.content_id == content_id).scalar()
    
    # Contar questões por tipo
    questions_by_type = db.query(
        Question.question_type,
        func.count(Question.id)
    ).filter(
        Question.content_id == content_id
    ).group_by(Question.question_type).all()
    
    # Total de visualizações dos vídeos
    total_views = db.query(func.sum(Video.view_count)).filter(Video.content_id == content_id).scalar() or 0
    
    return {
        "content_id": str(content_id),
        "title": content.title,
        "video_count": video_count,
        "question_count": sum(count for _, count in questions_by_type),
        "questions_by_type": {qtype: count for qtype, count in questions_by_type},
        "total_video_views": total_views,
        "difficulty_level": content.difficulty_level,
        "category": content.category
    }


