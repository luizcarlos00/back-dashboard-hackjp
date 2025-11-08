from fastapi import APIRouter, HTTPException
from app.config import supabase
from app.models import ProgressRequest, ProgressResponse
from datetime import datetime

router = APIRouter()

@router.post("", response_model=ProgressResponse)
async def record_progress(data: ProgressRequest):
    """
    Record that user watched a video.
    Increments video view count and returns watch statistics.
    """
    try:
        # Get user
        user = supabase.table("users") \
            .select("*") \
            .eq("device_id", data.device_id) \
            .execute()
        
        if not user.data or len(user.data) == 0:
            raise HTTPException(status_code=404, detail="User not found. Please create user first via POST /user")
        
        user_id = user.data[0]['id']
        videos_until_e2e = user.data[0].get('videos_until_e2e', 3)
        
        # Check if video exists
        video = supabase.table("videos") \
            .select("view_count") \
            .eq("id", data.video_id) \
            .execute()
        
        if not video.data or len(video.data) == 0:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Save progress
        supabase.table("user_progress") \
            .insert({
                "user_id": user_id,
                "video_id": data.video_id,
                "completed": data.completed,
                "watched_at": datetime.now().isoformat()
            }) \
            .execute()
        
        # Increment video view count
        current_view_count = video.data[0]['view_count']
        supabase.table("videos") \
            .update({"view_count": current_view_count + 1}) \
            .eq("id", data.video_id) \
            .execute()
        
        # Update user last active
        supabase.table("users") \
            .update({"last_active_at": datetime.now().isoformat()}) \
            .eq("id", user_id) \
            .execute()
        
        # Count total videos watched by user
        watched = supabase.table("user_progress") \
            .select("id", count="exact") \
            .eq("user_id", user_id) \
            .execute()
        
        watched_count = watched.count or 0
        
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
        raise HTTPException(status_code=500, detail=f"Error recording progress: {str(e)}")

