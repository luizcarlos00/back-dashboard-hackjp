from fastapi import APIRouter, HTTPException, Query
from app.config import supabase
from app.models import QuestionResponse
from app.services.n8n_client import n8n_client
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", response_model=QuestionResponse)
async def get_question(
    device_id: str = Query(..., description="User device ID"),
    video_id: str = Query(..., description="Video ID")
):
    """
    Generate personalized E2E question for user based on video watched.
    Calls n8n webhook with user profile and video context.
    Saves question to database and returns it.
    """
    try:
        # Get user profile
        user = supabase.table("users") \
            .select("*") \
            .eq("device_id", device_id) \
            .execute()
        
        if not user.data or len(user.data) == 0:
            raise HTTPException(status_code=404, detail="User not found. Please create user first via POST /user")
        
        user_data = user.data[0]
        user_id = user_data['id']
        
        # Get video details
        video = supabase.table("videos") \
            .select("*") \
            .eq("id", video_id) \
            .execute()
        
        if not video.data or len(video.data) == 0:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_data = video.data[0]
        
        # Call n8n to generate personalized question
        question_text = await n8n_client.generate_question(
            user_nome=user_data['nome'],
            user_idade=user_data['idade'],
            user_interesses=user_data.get('interesses', []),
            user_nivel_educacional=user_data['nivel_educacional'],
            video_title=video_data['title'],
            video_description=video_data.get('description', ''),
            expected_concepts=video_data.get('expected_concepts', [])
        )
        
        # Use fallback if n8n fails
        if not question_text:
            logger.warning(f"n8n failed, using fallback question for user {device_id}")
            question_text = n8n_client.get_fallback_question()
            generated_by = "manual"
        else:
            generated_by = "n8n"
        
        # Save question to database
        question = supabase.table("questions") \
            .insert({
                "user_id": user_id,
                "video_id": video_id,
                "question_text": question_text,
                "generated_by": generated_by,
                "created_at": datetime.now().isoformat()
            }) \
            .execute()
        
        if not question.data or len(question.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to save question")
        
        return QuestionResponse(**question.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")

@router.get("/prompts")
async def get_prompts():
    """
    Get list of available E2E prompts (for reference).
    """
    try:
        prompts = supabase.table("e2e_prompts") \
            .select("*") \
            .execute()
        
        return {"prompts": prompts.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prompts: {str(e)}")

