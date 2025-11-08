from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User, Video, Question, E2EPrompt
from app.models import QuestionResponse
from app.services.n8n_client import n8n_client
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", response_model=QuestionResponse)
async def get_question(
    device_id: str = Query(..., description="User device ID"),
    video_id: str = Query(..., description="Video ID"),
    db: Session = Depends(get_db)
):
    """Generate personalized E2E question for user based on video watched."""
    try:
        # Get user profile
        user = db.query(User).filter(User.device_id == device_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found. Please create user first via POST /user")
        
        # Get video details
        video = db.query(Video).filter(Video.id == uuid.UUID(video_id)).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Call n8n to generate personalized question
        question_text = await n8n_client.generate_question(
            user_nome=user.nome,
            user_idade=user.idade,
            user_interesses=user.interesses or [],
            user_nivel_educacional=user.nivel_educacional,
            video_title=video.title,
            video_description=video.description or '',
            expected_concepts=video.expected_concepts or []
        )
        
        # Use fallback if n8n fails
        if not question_text:
            logger.warning(f"n8n failed, using fallback question for user {device_id}")
            question_text = n8n_client.get_fallback_question()
            generated_by = "manual"
        else:
            generated_by = "n8n"
        
        # Save question to database
        question = Question(
            user_id=user.id,
            video_id=video.id,
            question_text=question_text,
            generated_by=generated_by,
            created_at=datetime.now()
        )
        
        db.add(question)
        db.commit()
        db.refresh(question)
        
        return QuestionResponse(
            id=str(question.id),
            user_id=str(question.user_id),
            video_id=str(question.video_id),
            question_text=question.question_text,
            generated_by=question.generated_by,
            created_at=question.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")

@router.get("/prompts")
async def get_prompts(db: Session = Depends(get_db)):
    """Get list of available E2E prompts (for reference)."""
    try:
        prompts = db.query(E2EPrompt).all()
        
        return {
            "prompts": [
                {
                    "id": str(p.id),
                    "text": p.text,
                    "category": p.category,
                    "created_at": p.created_at
                }
                for p in prompts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prompts: {str(e)}")
