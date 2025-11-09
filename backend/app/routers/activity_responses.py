from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import ActivityResponseCreate, ActivityResponseUpdate, UserActivityResponseDetail
from app.db_models import UserActivityResponse, Activity, User
from app.config import AUDIO_UPLOAD_DIR
import uuid
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=UserActivityResponseDetail, status_code=201)
def create_response(response_data: ActivityResponseCreate, db: Session = Depends(get_db)):
    """
    Cria uma resposta para uma atividade E2E
    """
    # Buscar usuário pelo device_id
    user = db.query(User).filter(User.device_id == response_data.device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se a atividade existe
    activity = db.query(Activity).filter(Activity.id == response_data.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    try:
        user_response = UserActivityResponse(
            id=str(uuid.uuid4()),
            user_id=user.id,
            activity_id=response_data.activity_id,
            answer=response_data.answer,
            grau_aprendizagem=response_data.grau_aprendizagem,
            responded=response_data.responded
        )
        db.add(user_response)
        db.commit()
        db.refresh(user_response)
        
        return UserActivityResponseDetail(
            id=user_response.id,
            user_id=user_response.user_id,
            activity_id=user_response.activity_id,
            answer=user_response.answer,
            grau_aprendizagem=user_response.grau_aprendizagem,
            responded=user_response.responded,
            created_at=user_response.created_at
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar resposta: {str(e)}")


@router.post("/audio", response_model=UserActivityResponseDetail, status_code=201)
async def create_audio_response(
    device_id: str,
    activity_id: str,
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Cria uma resposta em áudio para uma atividade E2E
    """
    # Buscar usuário pelo device_id
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se a atividade existe
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    try:
        # Salvar arquivo de áudio
        file_extension = os.path.splitext(audio.filename)[1]
        audio_filename = f"{uuid.uuid4()}{file_extension}"
        audio_path = os.path.join(AUDIO_UPLOAD_DIR, audio_filename)
        
        with open(audio_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        # URL relativa do áudio
        audio_url = f"/uploads/audio/{audio_filename}"
        
        # Criar resposta
        user_response = UserActivityResponse(
            id=str(uuid.uuid4()),
            user_id=user.id,
            activity_id=activity_id,
            answer=audio_url,  # URL do áudio
            responded=True
        )
        db.add(user_response)
        db.commit()
        db.refresh(user_response)
        
        return UserActivityResponseDetail(
            id=user_response.id,
            user_id=user_response.user_id,
            activity_id=user_response.activity_id,
            answer=user_response.answer,
            grau_aprendizagem=user_response.grau_aprendizagem,
            responded=user_response.responded,
            created_at=user_response.created_at
        )
    
    except Exception as e:
        db.rollback()
        # Tentar deletar o arquivo se algo der errado
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=f"Erro ao criar resposta de áudio: {str(e)}")


@router.get("/{response_id}", response_model=UserActivityResponseDetail)
def get_response(response_id: str, db: Session = Depends(get_db)):
    """
    Busca uma resposta por ID
    """
    response = db.query(UserActivityResponse).filter(UserActivityResponse.id == response_id).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    
    return UserActivityResponseDetail(
        id=response.id,
        user_id=response.user_id,
        activity_id=response.activity_id,
        answer=response.answer,
        grau_aprendizagem=response.grau_aprendizagem,
        responded=response.responded,
        created_at=response.created_at
    )


@router.get("/", response_model=List[UserActivityResponseDetail])
def list_responses(
    user_device_id: Optional[str] = None,
    activity_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista respostas de atividades
    
    Args:
        user_device_id: Filtrar por device_id do usuário
        activity_id: Filtrar por ID da atividade
        skip: Paginação
        limit: Limite de resultados
    """
    query = db.query(UserActivityResponse)
    
    if user_device_id:
        user = db.query(User).filter(User.device_id == user_device_id).first()
        if user:
            query = query.filter(UserActivityResponse.user_id == user.id)
    
    if activity_id:
        query = query.filter(UserActivityResponse.activity_id == activity_id)
    
    responses = query.order_by(UserActivityResponse.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        UserActivityResponseDetail(
            id=resp.id,
            user_id=resp.user_id,
            activity_id=resp.activity_id,
            answer=resp.answer,
            grau_aprendizagem=resp.grau_aprendizagem,
            responded=resp.responded,
            created_at=resp.created_at
        ) for resp in responses
    ]


@router.put("/{response_id}", response_model=UserActivityResponseDetail)
def update_response(
    response_id: str,
    update_data: ActivityResponseUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma resposta existente (ex: adicionar grau_aprendizagem depois da avaliação por IA)
    """
    response = db.query(UserActivityResponse).filter(UserActivityResponse.id == response_id).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    
    if update_data.answer is not None:
        response.answer = update_data.answer
    if update_data.grau_aprendizagem is not None:
        response.grau_aprendizagem = update_data.grau_aprendizagem
    if update_data.responded is not None:
        response.responded = update_data.responded
    
    try:
        db.commit()
        db.refresh(response)
        
        return UserActivityResponseDetail(
            id=response.id,
            user_id=response.user_id,
            activity_id=response.activity_id,
            answer=response.answer,
            grau_aprendizagem=response.grau_aprendizagem,
            responded=response.responded,
            created_at=response.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar resposta: {str(e)}")


@router.delete("/{response_id}", status_code=204)
def delete_response(response_id: str, db: Session = Depends(get_db)):
    """
    Deleta uma resposta
    """
    response = db.query(UserActivityResponse).filter(UserActivityResponse.id == response_id).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    
    try:
        # Se for áudio, tentar deletar o arquivo
        if response.answer and response.answer.startswith("/uploads/audio/"):
            audio_filename = response.answer.split("/")[-1]
            audio_path = os.path.join(AUDIO_UPLOAD_DIR, audio_filename)
            if os.path.exists(audio_path):
                os.remove(audio_path)
        
        db.delete(response)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar resposta: {str(e)}")

