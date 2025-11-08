from fastapi import APIRouter, HTTPException
from app.config import supabase
from app.models import UserCreate, UserResponse
from datetime import datetime

router = APIRouter()

@router.post("", response_model=UserResponse)
async def create_or_update_user(user_data: UserCreate):
    """
    Create or update user profile.
    Uses upsert logic: if device_id exists, updates profile; otherwise creates new user.
    """
    try:
        # Check if user already exists
        existing_user = supabase.table("users") \
            .select("*") \
            .eq("device_id", user_data.device_id) \
            .execute()
        
        if existing_user.data and len(existing_user.data) > 0:
            # Update existing user
            updated_user = supabase.table("users") \
                .update({
                    "nome": user_data.nome,
                    "idade": user_data.idade,
                    "interesses": user_data.interesses,
                    "nivel_educacional": user_data.nivel_educacional,
                    "last_active_at": datetime.now().isoformat()
                }) \
                .eq("device_id", user_data.device_id) \
                .execute()
            
            return UserResponse(**updated_user.data[0])
        else:
            # Create new user
            new_user = supabase.table("users") \
                .insert({
                    "device_id": user_data.device_id,
                    "nome": user_data.nome,
                    "idade": user_data.idade,
                    "interesses": user_data.interesses,
                    "nivel_educacional": user_data.nivel_educacional,
                    "last_active_at": datetime.now().isoformat()
                }) \
                .execute()
            
            return UserResponse(**new_user.data[0])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating/updating user: {str(e)}")

@router.get("/{device_id}", response_model=UserResponse)
async def get_user(device_id: str):
    """
    Get user profile by device_id.
    """
    try:
        user = supabase.table("users") \
            .select("*") \
            .eq("device_id", device_id) \
            .execute()
        
        if not user.data or len(user.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(**user.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

