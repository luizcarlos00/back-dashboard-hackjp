from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import VideoCreate, VideoResponse
from app.db_models import Video, Content
from app.services.youtube_service import get_video_info, extract_video_id
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=VideoResponse, status_code=201)
def create_video(video_data: VideoCreate, content_id: str, db: Session = Depends(get_db)):
    """
    Adiciona um novo vídeo a um conteúdo existente
    """
    # Verificar se o conteúdo existe
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    # Extrair o ID do vídeo se for uma URL
    video_id = extract_video_id(video_data.video_id)
    
    try:
        video = Video(
            id=str(uuid.uuid4()),
            content_id=content_id,
            video_id=video_id,
            title=video_data.title,
            quantity_until_e2e=video_data.quantity_until_e2e,
            order_index=video_data.order_index
        )
        db.add(video)
        db.commit()
        db.refresh(video)
        
        return _build_video_response(video)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar vídeo: {str(e)}")


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: str, include_url: bool = True, db: Session = Depends(get_db)):
    """
    Busca um vídeo por ID
    
    Args:
        video_id: ID do vídeo no banco
        include_url: Se True, busca a URL real via yt-dlp (default: True)
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    
    return _build_video_response(video, include_url=include_url)


@router.get("/", response_model=List[VideoResponse])
def list_videos(
    content_id: Optional[str] = None,
    include_url: bool = False,  # Por padrão não busca URL para listar (performance)
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista vídeos
    
    Args:
        content_id: Filtrar por ID do conteúdo
        include_url: Se True, busca URLs reais via yt-dlp (pode ser lento)
        skip: Paginação
        limit: Limite de resultados
    """
    query = db.query(Video)
    
    if content_id:
        query = query.filter(Video.content_id == content_id)
    
    videos = query.order_by(Video.order_index).offset(skip).limit(limit).all()
    
    return [_build_video_response(video, include_url=include_url) for video in videos]


@router.put("/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: str,
    title: Optional[str] = None,
    quantity_until_e2e: Optional[int] = None,
    order_index: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Atualiza um vídeo existente
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    
    if title is not None:
        video.title = title
    if quantity_until_e2e is not None:
        video.quantity_until_e2e = quantity_until_e2e
    if order_index is not None:
        video.order_index = order_index
    
    try:
        db.commit()
        db.refresh(video)
        return _build_video_response(video)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar vídeo: {str(e)}")


@router.delete("/{video_id}", status_code=204)
def delete_video(video_id: str, db: Session = Depends(get_db)):
    """
    Deleta um vídeo
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    
    try:
        db.delete(video)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar vídeo: {str(e)}")


def _build_video_response(video: Video, include_url: bool = True) -> VideoResponse:
    """
    Helper para construir a resposta do vídeo
    
    Args:
        video: Objeto Video do banco
        include_url: Se True, busca URL real via yt-dlp
    """
    response = VideoResponse(
        id=video.id,
        content_id=video.content_id,
        video_id=video.video_id,
        title=video.title,
        quantity_until_e2e=video.quantity_until_e2e,
        order_index=video.order_index,
        created_at=video.created_at
    )
    
    # Se solicitado, buscar informações do vídeo via yt-dlp
    if include_url:
        try:
            video_info = get_video_info(video.video_id)
            if video_info:
                response.url = video_info.get('url')
                response.thumbnail_url = video_info.get('thumbnail_url')
                response.duration = video_info.get('duration')
                
                # Se não tem título salvo, usa o do YouTube
                if not response.title and video_info.get('title'):
                    response.title = video_info.get('title')
        except Exception as e:
            logger.error(f"Erro ao buscar info do vídeo {video.video_id}: {str(e)}")
            # Continua sem a URL se falhar
            pass
    
    return response
