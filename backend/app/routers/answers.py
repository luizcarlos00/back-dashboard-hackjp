from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import AUDIO_UPLOAD_DIR
from app.db_models import User, Video, Question, Answer
from app.models import AnswerTextRequest, AnswerResponse
from app.services.langchain_analyzer import analyzer
from datetime import datetime
import uuid as uuid_lib
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("", response_model=AnswerResponse)
async def submit_text_answer(data: AnswerTextRequest, db: Session = Depends(get_db)):
    """Submit text answer to E2E question with LangChain analysis."""
    try:
        # Get user
        user = db.query(User).filter(User.device_id == data.device_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get question
        question = db.query(Question).filter(Question.id == data.question_id).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Get video for context
        video = db.query(Video).filter(Video.id == data.video_id).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Analyze response with LangChain
        logger.info(f"Analyzing text response for user {data.device_id}")
        analysis = await analyzer.analyze_response(
            user_response=data.text_response,
            video_title=video.title,
            video_description=video.description or '',
            expected_concepts=video.expected_concepts or [],
            question_text=question.question_text
        )
        
        # Save answer to database
        answer = Answer(
            user_id=user.id,
            question_id=question.id,
            video_id=video.id,
            response_type="text",
            text_response=data.text_response,
            ai_evaluation=analysis.feedback,
            concepts_identified=analysis.concepts_identified,
            quality_score=analysis.quality_score,
            passed=analysis.passed,
            created_at=datetime.now()
        )
        
        db.add(answer)
        db.commit()
        db.refresh(answer)
        
        logger.info(f"Text answer saved with score: {analysis.quality_score}")
        
        return AnswerResponse(
            id=str(answer.id),
            status="analyzed",
            quality_score=round(analysis.quality_score, 2),
            passed=analysis.passed,
            ai_evaluation=analysis.feedback,
            concepts_identified=analysis.concepts_identified,
            missing_concepts=analysis.missing_concepts,
            audio_url=None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting text answer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")

@router.post("/audio", response_model=AnswerResponse)
async def submit_audio_answer(
    device_id: str = Form(...),
    question_id: str = Form(...),
    video_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Submit audio answer to E2E question. Uploads to Supabase Storage."""
    try:
        # Get user
        user = db.query(User).filter(User.device_id == device_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate question exists
        question = db.query(Question).filter(Question.id == question_id).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Validate video exists
        video = db.query(Video).filter(Video.id == video_id).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Read file content
        contents = await file.read()
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'mp3'
        filename = f"{video.id}_{uuid_lib.uuid4()}.{file_extension}"
        
        # Create user directory if it doesn't exist
        user_audio_dir = os.path.join(AUDIO_UPLOAD_DIR, str(user.id))
        os.makedirs(user_audio_dir, exist_ok=True)
        
        # Full path to save the file
        file_path = os.path.join(user_audio_dir, filename)
        
        logger.info(f"Saving audio file: {file_path}")
        
        # Save file locally
        try:
            with open(file_path, "wb") as f:
                f.write(contents)
        except Exception as storage_error:
            logger.error(f"File save error: {str(storage_error)}")
            raise HTTPException(status_code=500, detail=f"Failed to save audio: {str(storage_error)}")
        
        # Generate relative URL for accessing the file
        audio_url = f"/uploads/audio/{user.id}/{filename}"
        
        # Save answer metadata to database
        answer = Answer(
            user_id=user.id,
            question_id=question.id,
            video_id=video.id,
            response_type="audio",
            audio_url=audio_url,
            audio_duration_seconds=30,
            created_at=datetime.now()
        )
        
        db.add(answer)
        db.commit()
        db.refresh(answer)
        
        logger.info(f"Audio answer saved successfully")
        
        return AnswerResponse(
            id=str(answer.id),
            status="saved",
            audio_url=audio_url,
            quality_score=None,
            passed=None,
            ai_evaluation="Áudio salvo com sucesso. Análise automática requer transcrição (recurso futuro).",
            concepts_identified=None,
            missing_concepts=None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting audio answer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting audio answer: {str(e)}")
