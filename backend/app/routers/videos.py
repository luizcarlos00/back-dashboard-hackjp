from fastapi import APIRouter, HTTPException, Query
from app.config import supabase
from app.models import VideoResponse, NextVideoResponse
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.get("", response_model=dict)
async def list_videos(
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List available videos with optional filtering.
    """
    try:
        # Build query
        query = supabase.table("videos") \
            .select("*", count="exact") \
            .eq("is_active", True)
        
        if category:
            query = query.eq("category", category)
        
        # Execute with pagination
        result = query \
            .order("created_at", desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        
        videos = [VideoResponse(**video) for video in result.data]
        
        return {
            "videos": videos,
            "total": result.count or 0,
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching videos: {str(e)}")

@router.get("/content", response_model=dict)
async def list_content(
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Alias for /videos endpoint - list available content.
    """
    return await list_videos(category=category, limit=limit, offset=offset)

@router.get("/next", response_model=NextVideoResponse)
async def get_next_video(device_id: str = Query(..., description="User device ID")):
    """
    Get next video for user to watch.
    Prioritizes unwatched videos, falls back to random if all watched.
    Returns E2E trigger flag based on user's watch count.
    """
    try:
        # Get or create user
        user = supabase.table("users") \
            .select("*") \
            .eq("device_id", device_id) \
            .execute()
        
        if not user.data or len(user.data) == 0:
            # Create minimal user if doesn't exist
            user = supabase.table("users") \
                .insert({
                    "device_id": device_id,
                    "nome": "User",
                    "idade": 0,
                    "nivel_educacional": "unknown",
                    "last_active_at": datetime.now().isoformat()
                }) \
                .execute()
        
        user_id = user.data[0]['id']
        videos_until_e2e = user.data[0].get('videos_until_e2e', 3)
        
        # Get watched video IDs
        watched = supabase.table("user_progress") \
            .select("video_id") \
            .eq("user_id", user_id) \
            .execute()
        
        watched_ids = [w['video_id'] for w in watched.data]
        watched_count = len(watched_ids)
        
        # Find unwatched video
        query = supabase.table("videos") \
            .select("*") \
            .eq("is_active", True)
        
        if watched_ids:
            # Get videos not in watched list
            all_videos = query.execute()
            unwatched_videos = [v for v in all_videos.data if v['id'] not in watched_ids]
            
            if unwatched_videos:
                video_data = unwatched_videos[0]
            else:
                # All watched, get random video
                video_data = all_videos.data[0] if all_videos.data else None
        else:
            # No videos watched yet, get first available
            result = query.limit(1).execute()
            video_data = result.data[0] if result.data else None
        
        if not video_data:
            raise HTTPException(status_code=404, detail="No videos available")
        
        video = VideoResponse(**video_data)
        
        # Determine if should trigger E2E
        should_trigger_e2e = (watched_count + 1) % videos_until_e2e == 0
        
        return NextVideoResponse(
            video=video,
            watched_count=watched_count,
            should_trigger_e2e=should_trigger_e2e
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting next video: {str(e)}")

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    """
    Get specific video by ID.
    """
    try:
        video = supabase.table("videos") \
            .select("*") \
            .eq("id", video_id) \
            .execute()
        
        if not video.data or len(video.data) == 0:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return VideoResponse(**video.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")

