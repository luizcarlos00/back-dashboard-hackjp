from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ContentCreate, ContentResponse, ContentUpdate, VideoResponse, ActivityResponse
from app.db_models import Content, Video, Activity
import uuid

router = APIRouter()


@router.post("/", response_model=ContentResponse, status_code=201)
def create_content(content_data: ContentCreate, db: Session = Depends(get_db)):
    """
    Cria um novo conteúdo com vídeos e atividades
    """
    try:
        # Criar o conteúdo
        content = Content(
            id=str(uuid.uuid4()),
            title=content_data.title,
            description=content_data.description,
            publico_alvo=content_data.publico_alvo,
            category=content_data.category,
            is_active=content_data.is_active
        )
        db.add(content)
        db.flush()  # Para obter o ID
        
        # Adicionar vídeos
        for video_data in content_data.videos:
            video = Video(
                id=str(uuid.uuid4()),
                content_id=content.id,
                video_id=video_data.video_id,
                title=video_data.title,
                quantity_until_e2e=video_data.quantity_until_e2e,
                order_index=video_data.order_index
            )
            db.add(video)
        
        # Adicionar atividades
        for activity_data in content_data.activities:
            activity = Activity(
                id=str(uuid.uuid4()),
                content_id=content.id,
                question=activity_data.question,
                order_index=activity_data.order_index
            )
            db.add(activity)
        
        db.commit()
        db.refresh(content)
        
        return _build_content_response(content)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar conteúdo: {str(e)}")


@router.get("/", response_model=List[ContentResponse])
def list_contents(
    skip: int = 0,
    limit: int = 100,
    publico_alvo: str = None,
    category: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos os conteúdos com filtros opcionais
    """
    query = db.query(Content)
    
    if publico_alvo:
        query = query.filter(Content.publico_alvo == publico_alvo)
    if category:
        query = query.filter(Content.category == category)
    if is_active is not None:
        query = query.filter(Content.is_active == is_active)
    
    contents = query.offset(skip).limit(limit).all()
    
    return [_build_content_response(content) for content in contents]


@router.get("/{content_id}", response_model=ContentResponse)
def get_content(content_id: str, db: Session = Depends(get_db)):
    """
    Busca um conteúdo específico por ID
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    return _build_content_response(content)


@router.put("/{content_id}", response_model=ContentResponse)
def update_content(content_id: str, content_data: ContentUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um conteúdo existente
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    # Atualizar campos fornecidos
    if content_data.title is not None:
        content.title = content_data.title
    if content_data.description is not None:
        content.description = content_data.description
    if content_data.publico_alvo is not None:
        content.publico_alvo = content_data.publico_alvo
    if content_data.category is not None:
        content.category = content_data.category
    if content_data.is_active is not None:
        content.is_active = content_data.is_active
    
    try:
        db.commit()
        db.refresh(content)
        return _build_content_response(content)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar conteúdo: {str(e)}")


@router.delete("/{content_id}", status_code=204)
def delete_content(content_id: str, db: Session = Depends(get_db)):
    """
    Deleta um conteúdo (e todos os vídeos e atividades relacionadas)
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    try:
        db.delete(content)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar conteúdo: {str(e)}")


def _build_content_response(content: Content) -> ContentResponse:
    """
    Helper para construir a resposta do conteúdo
    """
    return ContentResponse(
        id=content.id,
        title=content.title,
        description=content.description,
        publico_alvo=content.publico_alvo,
        category=content.category,
        is_active=content.is_active,
        created_at=content.created_at,
        updated_at=content.updated_at,
        videos=[
            VideoResponse(
                id=video.id,
                content_id=video.content_id,
                video_id=video.video_id,
                title=video.title,
                quantity_until_e2e=video.quantity_until_e2e,
                order_index=video.order_index,
                created_at=video.created_at
            ) for video in content.videos
        ],
        activities=[
            ActivityResponse(
                id=activity.id,
                content_id=activity.content_id,
                question=activity.question,
                order_index=activity.order_index,
                created_at=activity.created_at
            ) for activity in content.activities
        ]
    )
