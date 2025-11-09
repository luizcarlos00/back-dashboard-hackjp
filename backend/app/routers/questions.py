from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User, Video, Question
from app.models import QuestionResponse
from app.services.agent import generate_educational_questions
from datetime import datetime
import logging

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
        video = db.query(Video).filter(Video.id == video_id).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Generate personalized question using agent with user's educational level from database
        try:
            questions = generate_educational_questions(
                topic=video.title or "conteúdo do vídeo",
                num_questions=1,
                device_id=device_id,
                db=db,
                rag_path="app/data_rag/bncc.txt"  # Path to educational context
            )
            
            if questions and len(questions) > 0:
                question_data = questions[0]
                question_text = question_data.get("pergunta_gerada", 
                    f"Baseado no vídeo '{video.title}', explique o que você aprendeu e como pode aplicar esse conhecimento.")
            else:
                question_text = f"Baseado no vídeo '{video.title}', explique o que você aprendeu e como pode aplicar esse conhecimento."
        except Exception as e:
            logger.warning(f"Error generating AI question, using fallback: {str(e)}")
            question_text = f"Baseado no vídeo '{video.title}', explique o que você aprendeu e como pode aplicar esse conhecimento."
        
        # Save question to database
        question = Question(
            user_id=user.id,
            video_id=video.id,
            question_text=question_text,
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
    # E2E prompts are currently generated dynamically based on video content
    return {
        "prompts": [
            {
                "id": "1",
                "text": "Baseado no vídeo que você assistiu, explique o que você aprendeu e como pode aplicar esse conhecimento.",
                "category": "general"
            }
        ]
    }
