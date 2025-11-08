from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.db_models import User, Video, Answer, UserProgress, Question
from app.models import DashboardStats
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
async def get_stats(db: Session = Depends(get_db)):
    """Get aggregate statistics for dashboard."""
    try:
        # Total users
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        # Total videos watched
        total_videos_watched = db.query(func.count(UserProgress.id)).scalar() or 0
        
        # Total answers
        total_answers = db.query(func.count(Answer.id)).scalar() or 0
        
        # Count by response type
        answers_audio_count = db.query(func.count(Answer.id)).filter(Answer.response_type == 'audio').scalar() or 0
        answers_text_count = db.query(func.count(Answer.id)).filter(Answer.response_type == 'text').scalar() or 0
        
        # Calculate average quality score
        avg_quality_score_result = db.query(func.avg(Answer.quality_score)).filter(Answer.quality_score.isnot(None)).scalar()
        avg_quality_score = float(avg_quality_score_result) if avg_quality_score_result else 0.0
        
        # Calculate pass rate
        total_evaluated = db.query(func.count(Answer.id)).filter(Answer.passed.isnot(None)).scalar() or 0
        passed_count = db.query(func.count(Answer.id)).filter(Answer.passed == True).scalar() or 0
        pass_rate = passed_count / total_evaluated if total_evaluated else 0.0
        
        # Top categories by view count
        categories = db.query(
            Video.category,
            func.sum(Video.view_count).label('total_views')
        ).group_by(Video.category).order_by(func.sum(Video.view_count).desc()).limit(5).all()
        
        top_categories = [
            {"category": cat, "count": int(views) if views else 0}
            for cat, views in categories
        ]
        
        return DashboardStats(
            total_users=total_users,
            total_videos_watched=total_videos_watched,
            total_answers=total_answers,
            answers_audio_count=answers_audio_count,
            answers_text_count=answers_text_count,
            avg_quality_score=round(avg_quality_score, 2),
            pass_rate=round(pass_rate, 2),
            top_categories=top_categories
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.get("/e2e")
async def get_e2e_responses(
    response_type: Optional[str] = Query(None, description="Filter by 'audio' or 'text'"),
    passed: Optional[bool] = Query(None, description="Filter by pass/fail status"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get list of E2E answers for review."""
    try:
        # Build query with joins
        query = db.query(
            Answer,
            User.nome.label('user_nome'),
            Video.title.label('video_title'),
            Question.question_text.label('question_text')
        ).join(User, Answer.user_id == User.id) \
         .join(Video, Answer.video_id == Video.id) \
         .join(Question, Answer.question_id == Question.id)
        
        # Apply filters
        if response_type:
            if response_type not in ['audio', 'text']:
                raise HTTPException(status_code=400, detail="response_type must be 'audio' or 'text'")
            query = query.filter(Answer.response_type == response_type)
        
        if passed is not None:
            query = query.filter(Answer.passed == passed)
        
        # Execute query
        results = query.order_by(Answer.created_at.desc()).limit(limit).all()
        
        # Format response
        responses = []
        for answer, user_nome, video_title, question_text in results:
            responses.append({
                "id": str(answer.id),
                "user_id": str(answer.user_id),
                "user_nome": user_nome,
                "video_title": video_title,
                "question_text": question_text,
                "response_type": answer.response_type,
                "text_response": answer.text_response,
                "audio_url": answer.audio_url,
                "transcription": answer.transcription,
                "ai_evaluation": answer.ai_evaluation,
                "quality_score": answer.quality_score,
                "passed": answer.passed,
                "concepts_identified": answer.concepts_identified or [],
                "created_at": answer.created_at
            })
        
        return {
            "responses": responses,
            "total": len(responses),
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching E2E responses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching E2E responses: {str(e)}")
