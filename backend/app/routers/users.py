from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User
from app.models import UserCreate, UserResponse
from datetime import datetime

router = APIRouter()

@router.post("", response_model=UserResponse)
async def create_or_update_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create or update user profile"""
    try:
        existing_user = db.query(User).filter(User.device_id == user_data.device_id).first()
        
        if existing_user:
            existing_user.nome = user_data.nome
            existing_user.idade = user_data.idade
            existing_user.interesses = user_data.interesses
            existing_user.nivel_educacional = user_data.nivel_educacional
            existing_user.last_active_at = datetime.now()
            db.commit()
            db.refresh(existing_user)
            user_to_return = existing_user
        else:
            new_user = User(
                device_id=user_data.device_id,
                nome=user_data.nome,
                idade=user_data.idade,
                interesses=user_data.interesses,
                nivel_educacional=user_data.nivel_educacional,
                last_active_at=datetime.now()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_to_return = new_user
        
        return UserResponse(
            id=str(user_to_return.id),
            device_id=user_to_return.device_id,
            nome=user_to_return.nome,
            idade=user_to_return.idade,
            interesses=user_to_return.interesses,
            nivel_educacional=user_to_return.nivel_educacional,
            videos_until_e2e=user_to_return.videos_until_e2e,
            created_at=user_to_return.created_at,
            last_active_at=user_to_return.last_active_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/{device_id}", response_model=UserResponse)
async def get_user(device_id: str, db: Session = Depends(get_db)):
    """Get user profile by device_id"""
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=str(user.id),
        device_id=user.device_id,
        nome=user.nome,
        idade=user.idade,
        interesses=user.interesses,
        nivel_educacional=user.nivel_educacional,
        videos_until_e2e=user.videos_until_e2e,
        created_at=user.created_at,
        last_active_at=user.last_active_at
    )
