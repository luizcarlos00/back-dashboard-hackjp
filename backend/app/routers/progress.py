from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User, Video, UserProgress
from app.models import ProgressRequest, ProgressResponse
from datetime import datetime
import uuid

router = APIRouter()

@router.post("", response_model=ProgressResponse)
async def record_progress(data: ProgressRequest, db: Session = Depends(get_db)):
    """Record that user watched a video."""
    try:
        # Get user
        user = db.query(User).filter(User.device_id == data.device_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found. Please create user first via POST /user")
        
        videos_until_e2e = user.videos_until_e2e
        
        # Check if video exists
        video = db.query(Video).filter(Video.id == uuid.UUID(data.video_id)).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Save progress
        progress = UserProgress(
            user_id=user.id,
            video_id=video.id,
            completed=data.completed,
            watched_at=datetime.now()
        )
        db.add(progress)
        
        # Increment video view count
        video.view_count += 1
        
        # Update user last active
        user.last_active_at = datetime.now()
        
        db.commit()
        
        # Count total videos watched by user
        watched_count = db.query(UserProgress).filter(UserProgress.user_id == user.id).count()
        
        # Determine if should trigger E2E
        should_trigger_e2e = watched_count % videos_until_e2e == 0
        
        return ProgressResponse(
            success=True,
            watched_count=watched_count,
            should_trigger_e2e=should_trigger_e2e
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error recording progress: {str(e)}")
