from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.db_models import Video, User, UserProgress
from app.models import VideoResponse, NextVideoResponse
from typing import Optional
from datetime import datetime
import uuid

router = APIRouter()

@router.get("", response_model=dict)
async def list_videos(
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List available videos with optional filtering."""
    try:
        query = db.query(Video).filter(Video.is_active == True)
        
        if category:
            query = query.filter(Video.category == category)
        
        total = query.count()
        videos = query.order_by(Video.created_at.desc()).limit(limit).offset(offset).all()
        
        videos_response = [
            VideoResponse(
                id=str(v.id),
                title=v.title,
                description=v.description,
                url=v.url,
                thumbnail_url=v.thumbnail_url,
                duration_seconds=v.duration_seconds,
                category=v.category,
                difficulty=v.difficulty,
                keywords=v.keywords or [],
                expected_concepts=v.expected_concepts or [],
                view_count=v.view_count,
                created_at=v.created_at
            )
            for v in videos
        ]
        
        return {"videos": videos_response, "total": total, "limit": limit, "offset": offset}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching videos: {str(e)}")

@router.get("/content", response_model=dict)
async def list_content(
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Alias for /videos endpoint."""
    return await list_videos(category=category, limit=limit, offset=offset, db=db)

@router.get("/next", response_model=NextVideoResponse)
async def get_next_video(
    device_id: str = Query(..., description="User device ID"),
    db: Session = Depends(get_db)
):
    """Get next video for user to watch."""
    try:
        # Get or create user
        user = db.query(User).filter(User.device_id == device_id).first()
        
        if not user:
            user = User(
                device_id=device_id,
                nome="User",
                idade=0,
                nivel_educacional="unknown",
                last_active_at=datetime.now()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        videos_until_e2e = user.videos_until_e2e
        
        # Get watched video IDs
        watched_ids = [str(p.video_id) for p in db.query(UserProgress).filter(UserProgress.user_id == user.id).all()]
        watched_count = len(watched_ids)
        
        # Find unwatched video
        query = db.query(Video).filter(Video.is_active == True)
        
        if watched_ids:
            watched_uuids = [uuid.UUID(vid) for vid in watched_ids]
            query = query.filter(~Video.id.in_(watched_uuids))
        
        video = query.first()
        
        if not video:
            # All watched, get any active video
            video = db.query(Video).filter(Video.is_active == True).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="No videos available")
        
        video_response = VideoResponse(
            id=str(video.id),
            title=video.title,
            description=video.description,
            url=video.url,
            thumbnail_url=video.thumbnail_url,
            duration_seconds=video.duration_seconds,
            category=video.category,
            difficulty=video.difficulty,
            keywords=video.keywords or [],
            expected_concepts=video.expected_concepts or [],
            view_count=video.view_count,
            created_at=video.created_at
        )
        
        should_trigger_e2e = (watched_count + 1) % videos_until_e2e == 0
        
        return NextVideoResponse(
            video=video_response,
            watched_count=watched_count,
            should_trigger_e2e=should_trigger_e2e
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting next video: {str(e)}")

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str, db: Session = Depends(get_db)):
    """Get specific video by ID."""
    try:
        video = db.query(Video).filter(Video.id == uuid.UUID(video_id)).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return VideoResponse(
            id=str(video.id),
            title=video.title,
            description=video.description,
            url=video.url,
            thumbnail_url=video.thumbnail_url,
            duration_seconds=video.duration_seconds,
            category=video.category,
            difficulty=video.difficulty,
            keywords=video.keywords or [],
            expected_concepts=video.expected_concepts or [],
            view_count=video.view_count,
            created_at=video.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")
