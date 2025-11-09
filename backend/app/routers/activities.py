from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import ActivityCreate, ActivityResponse
from app.db_models import Activity, Content
import uuid

router = APIRouter()


@router.post("/", response_model=ActivityResponse, status_code=201)
def create_activity(activity_data: ActivityCreate, content_id: str, db: Session = Depends(get_db)):
    """
    Adiciona uma nova atividade E2E a um conteúdo existente
    """
    # Verificar se o conteúdo existe
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado")
    
    try:
        activity = Activity(
            id=str(uuid.uuid4()),
            content_id=content_id,
            question=activity_data.question,
            order_index=activity_data.order_index
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        
        return ActivityResponse(
            id=activity.id,
            content_id=activity.content_id,
            question=activity.question,
            order_index=activity.order_index,
            created_at=activity.created_at
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar atividade: {str(e)}")


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: str, db: Session = Depends(get_db)):
    """
    Busca uma atividade por ID
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    return ActivityResponse(
        id=activity.id,
        content_id=activity.content_id,
        question=activity.question,
        order_index=activity.order_index,
        created_at=activity.created_at
    )


@router.get("/", response_model=List[ActivityResponse])
def list_activities(
    content_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista atividades E2E
    
    Args:
        content_id: Filtrar por ID do conteúdo
        skip: Paginação
        limit: Limite de resultados
    """
    query = db.query(Activity)
    
    if content_id:
        query = query.filter(Activity.content_id == content_id)
    
    activities = query.order_by(Activity.order_index).offset(skip).limit(limit).all()
    
    return [
        ActivityResponse(
            id=activity.id,
            content_id=activity.content_id,
            question=activity.question,
            order_index=activity.order_index,
            created_at=activity.created_at
        ) for activity in activities
    ]


@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: str,
    question: Optional[str] = None,
    order_index: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma atividade existente
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    if question is not None:
        activity.question = question
    if order_index is not None:
        activity.order_index = order_index
    
    try:
        db.commit()
        db.refresh(activity)
        
        return ActivityResponse(
            id=activity.id,
            content_id=activity.content_id,
            question=activity.question,
            order_index=activity.order_index,
            created_at=activity.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar atividade: {str(e)}")


@router.delete("/{activity_id}", status_code=204)
def delete_activity(activity_id: str, db: Session = Depends(get_db)):
    """
    Deleta uma atividade
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    try:
        db.delete(activity)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar atividade: {str(e)}")

