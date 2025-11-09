"""
Router específico para integração com o frontend do dashboard
Transforma os dados da nova estrutura para o formato esperado pelo frontend
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.db_models import User, Content, Video, Activity, UserVideoProgress, UserActivityResponse

router = APIRouter()


@router.get("/students")
def get_students_for_dashboard(db: Session = Depends(get_db)):
    """
    Retorna dados dos estudantes no formato esperado pelo dashboard frontend
    
    Formato esperado:
    {
      id: number,
      nome: string,
      idade: number,
      escolaridade: 'Fundamental' | 'Médio' | 'Superior',
      conteudos: [{
        id: string,
        tipo: 'video' | 'atividade' | 'exercicio',
        titulo: string,
        dificuldade: 'Fácil' | 'Médio' | 'Difícil',
        concluido: boolean,
        dataInicio?: string
      }]
    }
    """
    users = db.query(User).all()
    
    students_data = []
    
    for idx, user in enumerate(users, 1):
        # Mapear nivel_educacional para escolaridade
        escolaridade_map = {
            'fundamental': 'Fundamental',
            'medio': 'Médio',
            'médio': 'Médio',
            'superior': 'Superior',
            'tecnico': 'Superior',
            'técnico': 'Superior'
        }
        escolaridade = escolaridade_map.get(
            user.nivel_educacional.lower() if user.nivel_educacional else 'medio',
            'Médio'
        )
        
        # Coletar conteúdos do usuário
        conteudos = []
        
        # 1. Vídeos assistidos (tipo: video)
        videos_watched = db.query(UserVideoProgress, Video).join(
            Video, UserVideoProgress.video_id == Video.id
        ).filter(
            UserVideoProgress.user_id == user.id,
            UserVideoProgress.watched == True
        ).all()
        
        for progress, video in videos_watched:
            conteudos.append({
                'id': f'video-{video.id}',
                'tipo': 'video',
                'titulo': video.title or f'Vídeo {video.video_id}',
                'dificuldade': _map_difficulty_from_order(video.order_index),
                'concluido': True,
                'dataInicio': progress.watched_at.strftime('%Y-%m-%d') if progress.watched_at else None
            })
        
        # 2. Atividades respondidas (tipo: atividade)
        activities_responded = db.query(UserActivityResponse, Activity).join(
            Activity, UserActivityResponse.activity_id == Activity.id
        ).filter(
            UserActivityResponse.user_id == user.id,
            UserActivityResponse.responded == True
        ).all()
        
        for response, activity in activities_responded:
            # Mapear grau_aprendizagem para dificuldade
            dificuldade = _map_difficulty_from_learning_grade(response.grau_aprendizagem)
            
            conteudos.append({
                'id': f'activity-{activity.id}',
                'tipo': 'atividade',
                'titulo': activity.question[:50] + '...' if len(activity.question) > 50 else activity.question,
                'dificuldade': dificuldade,
                'concluido': True,
                'dataInicio': response.created_at.strftime('%Y-%m-%d') if response.created_at else None
            })
        
        # 3. Adicionar conteúdos pendentes (vídeos não assistidos)
        # Buscar conteúdos que o usuário tem acesso mas não completou
        all_videos = db.query(Video).limit(5).all()  # Limitar para performance
        
        for video in all_videos:
            # Verificar se já não foi adicionado como assistido
            already_added = any(c['id'] == f'video-{video.id}' for c in conteudos)
            if not already_added:
                # Verificar se existe progresso
                has_progress = db.query(UserVideoProgress).filter(
                    UserVideoProgress.user_id == user.id,
                    UserVideoProgress.video_id == video.id
                ).first()
                
                if not has_progress:
                    conteudos.append({
                        'id': f'video-{video.id}',
                        'tipo': 'video',
                        'titulo': video.title or f'Vídeo {video.video_id}',
                        'dificuldade': _map_difficulty_from_order(video.order_index),
                        'concluido': False
                    })
        
        student_data = {
            'id': idx,  # ID sequencial para o frontend
            'nome': user.nome,
            'idade': user.idade or 18,
            'escolaridade': escolaridade,
            'conteudos': conteudos
        }
        
        students_data.append(student_data)
    
    return students_data


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas gerais para o dashboard
    """
    total_students = db.query(func.count(User.id)).scalar() or 0
    total_videos = db.query(func.count(Video.id)).scalar() or 0
    total_activities = db.query(func.count(Activity.id)).scalar() or 0
    
    # Total de vídeos assistidos
    videos_watched = db.query(func.count(UserVideoProgress.id)).filter(
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    # Total de atividades respondidas
    activities_completed = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    # Média de grau de aprendizagem
    avg_learning = db.query(func.avg(UserActivityResponse.grau_aprendizagem)).filter(
        UserActivityResponse.grau_aprendizagem.isnot(None)
    ).scalar() or 0.0
    
    return {
        'totalStudents': total_students,
        'totalVideos': total_videos,
        'totalActivities': total_activities,
        'videosWatched': videos_watched,
        'activitiesCompleted': activities_completed,
        'avgLearningGrade': round(float(avg_learning), 2) if avg_learning else 0.0,
        'completionRate': round((activities_completed / total_activities * 100), 2) if total_activities > 0 else 0
    }


def _map_difficulty_from_order(order_index: int) -> str:
    """
    Mapeia o order_index para dificuldade
    """
    if order_index <= 2:
        return 'Fácil'
    elif order_index <= 5:
        return 'Médio'
    else:
        return 'Difícil'


def _map_difficulty_from_learning_grade(grau: float = None) -> str:
    """
    Mapeia grau_aprendizagem para dificuldade
    Quanto maior o grau, mais fácil foi (usuário aprendeu bem)
    """
    if grau is None:
        return 'Médio'
    
    if grau >= 0.8:
        return 'Fácil'
    elif grau >= 0.5:
        return 'Médio'
    else:
        return 'Difícil'


@router.get("/content-distribution")
def get_content_distribution(db: Session = Depends(get_db)):
    """
    Retorna distribuição de tipos de conteúdo
    """
    total_videos = db.query(func.count(UserVideoProgress.id)).filter(
        UserVideoProgress.watched == True
    ).scalar() or 0
    
    total_activities = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    return {
        'video': total_videos,
        'atividade': total_activities,
        'exercicio': total_activities  # Por enquanto, usar o mesmo que atividades
    }


@router.get("/difficulty-distribution")
def get_difficulty_distribution(db: Session = Depends(get_db)):
    """
    Retorna distribuição de dificuldades baseada em grau_aprendizagem
    """
    # Contar respostas por faixa de grau
    facil = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.grau_aprendizagem >= 0.8,
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    medio = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.grau_aprendizagem >= 0.5,
        UserActivityResponse.grau_aprendizagem < 0.8,
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    dificil = db.query(func.count(UserActivityResponse.id)).filter(
        UserActivityResponse.grau_aprendizagem < 0.5,
        UserActivityResponse.responded == True
    ).scalar() or 0
    
    return {
        'Fácil': facil,
        'Médio': medio,
        'Difícil': dificil
    }

