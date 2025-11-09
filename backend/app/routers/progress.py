from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models import VideoProgressCreate, VideoProgressResponse, NextVideoResponse, VideoResponse, ActivityResponse
from app.db_models import UserVideoProgress, User, Video, Activity, Content, UserActivityResponse
from app.routers.videos import _build_video_response
import uuid

router = APIRouter()


@router.post("/watch", response_model=VideoProgressResponse, status_code=201)
def mark_video_watched(progress_data: VideoProgressCreate, db: Session = Depends(get_db)):
    """
    Marca um vídeo como assistido para um usuário
    """
    # Buscar usuário pelo device_id
    user = db.query(User).filter(User.device_id == progress_data.device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se o vídeo existe
    video = db.query(Video).filter(Video.id == progress_data.video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    
    # Verificar se já existe progresso
    existing_progress = db.query(UserVideoProgress).filter(
        UserVideoProgress.user_id == user.id,
        UserVideoProgress.video_id == progress_data.video_id
    ).first()
    
    if existing_progress:
        # Atualizar progresso existente
        existing_progress.watched = progress_data.watched
        db.commit()
        db.refresh(existing_progress)
        
        return VideoProgressResponse(
            id=existing_progress.id,
            user_id=existing_progress.user_id,
            video_id=existing_progress.video_id,
            watched=existing_progress.watched,
            watched_at=existing_progress.watched_at
        )
    
    # Criar novo progresso
    try:
        progress = UserVideoProgress(
            id=str(uuid.uuid4()),
            user_id=user.id,
            video_id=progress_data.video_id,
            watched=progress_data.watched
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        return VideoProgressResponse(
            id=progress.id,
            user_id=progress.user_id,
            video_id=progress.video_id,
            watched=progress.watched,
            watched_at=progress.watched_at
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao registrar progresso: {str(e)}")


@router.get("/next-video", response_model=NextVideoResponse)
def get_next_video(device_id: str, content_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retorna o próximo vídeo não assistido e verifica se deve disparar E2E
    
    Args:
        device_id: ID do dispositivo do usuário
        content_id: ID do conteúdo (opcional, se não fornecido pega qualquer vídeo)
    """
    # Buscar usuário
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Query para vídeos
    query = db.query(Video).filter(Video.id.notin_(
        db.query(UserVideoProgress.video_id).filter(
            UserVideoProgress.user_id == user.id,
            UserVideoProgress.watched == True
        )
    ))
    
    if content_id:
        query = query.filter(Video.content_id == content_id)
    
    next_video = query.order_by(Video.order_index).first()
    
    # Contar vídeos assistidos
    watched_count = db.query(func.count(UserVideoProgress.id)).filter(
        UserVideoProgress.user_id == user.id,
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    # Verificar se deve disparar E2E
    should_trigger_e2e = False
    next_activity = None
    
    if next_video and watched_count > 0:
        # Verificar se atingiu a quantidade necessária
        should_trigger_e2e = (watched_count % next_video.quantity_until_e2e) == 0
        
        # Se deve disparar E2E, buscar próxima atividade não respondida
        if should_trigger_e2e and next_video.content_id:
            activity = db.query(Activity).filter(
                Activity.content_id == next_video.content_id,
                Activity.id.notin_(
                    db.query(UserActivityResponse.activity_id).filter(
                        UserActivityResponse.user_id == user.id,
                        UserActivityResponse.responded == True
                    )
                )
            ).order_by(Activity.order_index).first()
            
            if activity:
                next_activity = ActivityResponse(
                    id=activity.id,
                    content_id=activity.content_id,
                    question=activity.question,
                    order_index=activity.order_index,
                    created_at=activity.created_at
                )
    
    video_response = _build_video_response(next_video, include_url=True) if next_video else None
    
    return NextVideoResponse(
        video=video_response,
        watched_count=watched_count,
        should_trigger_e2e=should_trigger_e2e,
        next_activity=next_activity
    )


@router.get("/user/{device_id}", response_model=List[VideoProgressResponse])
def get_user_progress(device_id: str, content_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retorna todo o progresso de um usuário
    
    Args:
        device_id: ID do dispositivo do usuário
        content_id: Filtrar por conteúdo específico (opcional)
    """
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    query = db.query(UserVideoProgress).filter(UserVideoProgress.user_id == user.id)
    
    if content_id:
        query = query.join(Video).filter(Video.content_id == content_id)
    
    progress_list = query.all()
    
    return [
        VideoProgressResponse(
            id=progress.id,
            user_id=progress.user_id,
            video_id=progress.video_id,
            watched=progress.watched,
            watched_at=progress.watched_at
        ) for progress in progress_list
    ]


@router.get("/stats/{device_id}")
def get_user_stats(device_id: str, db: Session = Depends(get_db)):
    """
    Retorna estatísticas de progresso do usuário
    """
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Total de vídeos assistidos
    total_watched = db.query(func.count(UserVideoProgress.id)).filter(
        UserVideoProgress.user_id == user.id,
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    # Total de atividades respondidas
    total_responses = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.user_id == user.id,
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    # Média de grau de aprendizagem
    avg_learning = db.query(func.avg(UserActivityResponse.grau_aprendizagem)).filter(
        UserActivityResponse.user_id == user.id,
        UserActivityResponse.grau_aprendizagem.isnot(None)
    ).scalar() or 0.0
    
    # Conteúdos em progresso (tem pelo menos 1 vídeo assistido)
    contents_in_progress = db.query(Content).join(Video).join(UserVideoProgress).filter(
        UserVideoProgress.user_id == user.id,
        UserVideoProgress.watched == True
    ).distinct().count()
    
    return {
        "user_id": user.id,
        "device_id": user.device_id,
        "total_videos_watched": total_watched,
        "total_activities_completed": total_responses,
        "avg_learning_grade": round(float(avg_learning), 2),
        "contents_in_progress": contents_in_progress
    }
