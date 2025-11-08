from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.config import supabase
from app.models import AnswerTextRequest, AnswerResponse
from app.services.langchain_analyzer import analyzer
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("", response_model=AnswerResponse)
async def submit_text_answer(data: AnswerTextRequest):
    """
    Submit text answer to E2E question.
    Analyzes response with LangChain and saves to database.
    """
    try:
        # Get user
        user = supabase.table("users") \
            .select("*") \
            .eq("device_id", data.device_id) \
            .execute()
        
        if not user.data or len(user.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_id = user.data[0]['id']
        
        # Get question
        question = supabase.table("questions") \
            .select("*") \
            .eq("id", data.question_id) \
            .execute()
        
        if not question.data or len(question.data) == 0:
            raise HTTPException(status_code=404, detail="Question not found")
        
        question_data = question.data[0]
        
        # Get video for context
        video = supabase.table("videos") \
            .select("*") \
            .eq("id", data.video_id) \
            .execute()
        
        if not video.data or len(video.data) == 0:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_data = video.data[0]
        
        # Analyze response with LangChain
        logger.info(f"Analyzing text response for user {data.device_id}")
        analysis = await analyzer.analyze_response(
            user_response=data.text_response,
            video_title=video_data['title'],
            video_description=video_data.get('description', ''),
            expected_concepts=video_data.get('expected_concepts', []),
            question_text=question_data['question_text']
        )
        
        # Save answer to database
        answer = supabase.table("answers") \
            .insert({
                "user_id": user_id,
                "question_id": data.question_id,
                "video_id": data.video_id,
                "response_type": "text",
                "text_response": data.text_response,
                "ai_evaluation": analysis.feedback,
                "concepts_identified": analysis.concepts_identified,
                "quality_score": analysis.quality_score,
                "passed": analysis.passed,
                "created_at": datetime.now().isoformat()
            }) \
            .execute()
        
        if not answer.data or len(answer.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to save answer")
        
        logger.info(f"Text answer saved with score: {analysis.quality_score}")
        
        return AnswerResponse(
            id=answer.data[0]['id'],
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
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")

@router.post("/audio", response_model=AnswerResponse)
async def submit_audio_answer(
    device_id: str = Form(...),
    question_id: str = Form(...),
    video_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Submit audio answer to E2E question.
    Uploads audio to Supabase Storage and saves metadata.
    Note: Transcription and analysis are optional/future features.
    """
    try:
        # Get user
        user = supabase.table("users") \
            .select("*") \
            .eq("device_id", device_id) \
            .execute()
        
        if not user.data or len(user.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_id = user.data[0]['id']
        
        # Validate question exists
        question = supabase.table("questions") \
            .select("id") \
            .eq("id", question_id) \
            .execute()
        
        if not question.data or len(question.data) == 0:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Validate video exists
        video = supabase.table("videos") \
            .select("id") \
            .eq("id", video_id) \
            .execute()
        
        if not video.data or len(video.data) == 0:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Read file content
        contents = await file.read()
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'mp3'
        file_path = f"{user_id}/{video_id}_{uuid.uuid4()}.{file_extension}"
        
        logger.info(f"Uploading audio file: {file_path}")
        
        # Upload to Supabase Storage
        try:
            storage_response = supabase.storage \
                .from_("e2e-audio") \
                .upload(file_path, contents, {"content-type": file.content_type or "audio/mpeg"})
        except Exception as storage_error:
            logger.error(f"Storage upload error: {str(storage_error)}")
            raise HTTPException(status_code=500, detail=f"Failed to upload audio: {str(storage_error)}")
        
        # Get public URL
        audio_url = supabase.storage \
            .from_("e2e-audio") \
            .get_public_url(file_path)
        
        # Save answer metadata to database
        answer = supabase.table("answers") \
            .insert({
                "user_id": user_id,
                "question_id": question_id,
                "video_id": video_id,
                "response_type": "audio",
                "audio_url": audio_url,
                "audio_duration_seconds": 30,  # Placeholder - could be extracted from file
                "created_at": datetime.now().isoformat()
            }) \
            .execute()
        
        if not answer.data or len(answer.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to save answer")
        
        logger.info(f"Audio answer saved successfully")
        
        return AnswerResponse(
            id=answer.data[0]['id'],
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
        raise HTTPException(status_code=500, detail=f"Error submitting audio answer: {str(e)}")

