from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from app.database import get_db
from app.models import DashboardStats, UserStats
from app.db_models import User, Content, Video, Activity, UserVideoProgress, UserActivityResponse
from datetime import datetime

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas gerais do dashboard
    """
    # Total de usuários
    total_users = db.query(func.count(User.id)).scalar() or 0
    
    # Total de vídeos
    total_videos = db.query(func.count(Video.id)).scalar() or 0
    
    # Total de atividades
    total_activities = db.query(func.count(Activity.id)).scalar() or 0
    
    # Total de visualizações de vídeos
    total_video_watches = db.query(func.count(UserVideoProgress.id)).filter(
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    # Total de respostas de atividades
    total_activity_responses = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    # Média de grau de aprendizagem
    avg_learning = db.query(func.avg(UserActivityResponse.grau_aprendizagem)).filter(
        UserActivityResponse.grau_aprendizagem.isnot(None)
    ).scalar() or 0.0
    
    # Conteúdo mais popular (mais vídeos assistidos)
    most_popular = db.query(
        Content.title,
        func.count(UserVideoProgress.id).label('watch_count')
    ).join(Video).join(UserVideoProgress).filter(
        UserVideoProgress.watched == True
    ).group_by(Content.id).order_by(desc('watch_count')).first()
    
    most_popular_content = most_popular[0] if most_popular else None
    
    return DashboardStats(
        total_users=total_users,
        total_videos=total_videos,
        total_activities=total_activities,
        total_video_watches=total_video_watches,
        total_activity_responses=total_activity_responses,
        avg_grau_aprendizagem=round(float(avg_learning), 2) if avg_learning else None,
        most_popular_content=most_popular_content
    )


@router.get("/users", response_model=List[UserStats])
def get_users_stats(
    skip: int = 0,
    limit: int = 50,
    order_by: str = "videos_watched",  # videos_watched, activities_completed, avg_grade
    db: Session = Depends(get_db)
):
    """
    Retorna estatísticas de todos os usuários
    
    Args:
        skip: Paginação
        limit: Limite de resultados
        order_by: Ordenar por (videos_watched, activities_completed, avg_grade)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    
    users_stats = []
    for user in users:
        # Vídeos assistidos
        videos_watched = db.query(func.count(UserVideoProgress.id)).filter(
            UserVideoProgress.user_id == user.id,
            UserVideoProgress.watched == True
        ).scalar() or 0
        
        # Atividades completadas
        activities_completed = db.query(func.count(UserActivityResponse.id)).filter(
            UserActivityResponse.user_id == user.id,
            UserActivityResponse.responded == True
        ).scalar() or 0
        
        # Média de grau de aprendizagem
        avg_learning = db.query(func.avg(UserActivityResponse.grau_aprendizagem)).filter(
            UserActivityResponse.user_id == user.id,
            UserActivityResponse.grau_aprendizagem.isnot(None)
        ).scalar()
        
        users_stats.append(UserStats(
            user_id=user.id,
            user_nome=user.nome,
            videos_watched=videos_watched,
            activities_completed=activities_completed,
            avg_grau_aprendizagem=round(float(avg_learning), 2) if avg_learning else None,
            last_active=user.last_active_at
        ))
    
    # Ordenar
    if order_by == "videos_watched":
        users_stats.sort(key=lambda x: x.videos_watched, reverse=True)
    elif order_by == "activities_completed":
        users_stats.sort(key=lambda x: x.activities_completed, reverse=True)
    elif order_by == "avg_grade":
        users_stats.sort(key=lambda x: x.avg_grau_aprendizagem or 0, reverse=True)
    
    return users_stats


@router.get("/content/{content_id}/stats")
def get_content_stats(content_id: str, db: Session = Depends(get_db)):
    """
    Retorna estatísticas de um conteúdo específico
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        return {"error": "Conteúdo não encontrado"}
    
    # Total de vídeos
    total_videos = db.query(func.count(Video.id)).filter(
        Video.content_id == content_id
    ).scalar() or 0
    
    # Total de atividades
    total_activities = db.query(func.count(Activity.id)).filter(
        Activity.content_id == content_id
    ).scalar() or 0
    
    # Total de visualizações
    total_watches = db.query(func.count(UserVideoProgress.id)).join(Video).filter(
        Video.content_id == content_id,
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    # Total de respostas
    total_responses = db.query(func.count(UserActivityResponse.id)).join(Activity).filter(
        Activity.content_id == content_id,
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    # Média de grau de aprendizagem
    avg_learning = db.query(func.avg(UserActivityResponse.grau_aprendizagem)).join(Activity).filter(
        Activity.content_id == content_id,
        UserActivityResponse.grau_aprendizagem.isnot(None)
    ).scalar()
    
    # Usuários únicos que assistiram
    unique_users = db.query(func.count(func.distinct(UserVideoProgress.user_id))).join(Video).filter(
        Video.content_id == content_id,
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    return {
        "content_id": content_id,
        "content_title": content.title,
        "publico_alvo": content.publico_alvo,
        "total_videos": total_videos,
        "total_activities": total_activities,
        "total_watches": total_watches,
        "total_responses": total_responses,
        "avg_grau_aprendizagem": round(float(avg_learning), 2) if avg_learning else None,
        "unique_users": unique_users,
        "completion_rate": round((total_responses / total_activities * 100), 2) if total_activities > 0 else 0
    }


@router.get("/leaderboard")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna um ranking dos usuários com melhor desempenho
    """
    # Buscar usuários com pelo menos 1 resposta
    users_with_responses = db.query(
        User.id,
        User.nome,
        func.count(UserActivityResponse.id).label('total_responses'),
        func.avg(UserActivityResponse.grau_aprendizagem).label('avg_grade')
    ).join(UserActivityResponse).filter(
        UserActivityResponse.responded == True,
        UserActivityResponse.grau_aprendizagem.isnot(None)
    ).group_by(User.id).having(
        func.count(UserActivityResponse.id) > 0
    ).all()
    
    # Criar ranking
    leaderboard = []
    for user in users_with_responses:
        leaderboard.append({
            "user_id": user.id,
            "user_nome": user.nome,
            "total_responses": user.total_responses,
            "avg_grau_aprendizagem": round(float(user.avg_grade), 2)
        })
    
    # Ordenar por média de aprendizagem
    leaderboard.sort(key=lambda x: x['avg_grau_aprendizagem'], reverse=True)
    
    return leaderboard[:limit]
