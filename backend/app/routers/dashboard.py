from fastapi import APIRouter, HTTPException, Query
from app.config import supabase
from app.models import DashboardStats, DashboardAnswer
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
async def get_stats():
    """
    Get aggregate statistics for dashboard.
    Includes user counts, videos watched, answer metrics, etc.
    """
    try:
        # Total users
        users = supabase.table("users") \
            .select("id", count="exact") \
            .execute()
        total_users = users.count or 0
        
        # Total videos watched
        progress = supabase.table("user_progress") \
            .select("id", count="exact") \
            .execute()
        total_videos_watched = progress.count or 0
        
        # Total answers
        answers = supabase.table("answers") \
            .select("*", count="exact") \
            .execute()
        total_answers = answers.count or 0
        
        # Count by response type
        answers_audio_count = len([a for a in answers.data if a['response_type'] == 'audio'])
        answers_text_count = len([a for a in answers.data if a['response_type'] == 'text'])
        
        # Calculate average quality score (only for text answers with scores)
        scores = [a['quality_score'] for a in answers.data if a.get('quality_score') is not None]
        avg_quality_score = sum(scores) / len(scores) if scores else 0.0
        
        # Calculate pass rate (only for answers with pass/fail status)
        evaluated_answers = [a for a in answers.data if a.get('passed') is not None]
        passed_count = len([a for a in evaluated_answers if a['passed']])
        pass_rate = passed_count / len(evaluated_answers) if evaluated_answers else 0.0
        
        # Top categories by view count
        videos = supabase.table("videos") \
            .select("category, view_count") \
            .execute()
        
        categories = {}
        for v in videos.data:
            cat = v['category']
            categories[cat] = categories.get(cat, 0) + v['view_count']
        
        top_categories = [
            {"category": k, "count": v}
            for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)
        ][:5]
        
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
    limit: int = Query(50, ge=1, le=200)
):
    """
    Get list of E2E answers for review.
    Includes user info, video, question, and AI evaluation.
    """
    try:
        # Build query with joins
        query = supabase.table("answers") \
            .select("""
                *,
                users!inner(id, nome),
                videos!inner(id, title),
                questions!inner(id, question_text)
            """)
        
        # Apply filters
        if response_type:
            if response_type not in ['audio', 'text']:
                raise HTTPException(status_code=400, detail="response_type must be 'audio' or 'text'")
            query = query.eq("response_type", response_type)
        
        if passed is not None:
            query = query.eq("passed", passed)
        
        # Execute query
        result = query \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        # Format response
        responses = []
        for r in result.data:
            responses.append({
                "id": r['id'],
                "user_id": r['user_id'],
                "user_nome": r['users']['nome'] if r.get('users') else None,
                "video_title": r['videos']['title'] if r.get('videos') else "Unknown",
                "question_text": r['questions']['question_text'] if r.get('questions') else "Unknown",
                "response_type": r['response_type'],
                "text_response": r.get('text_response'),
                "audio_url": r.get('audio_url'),
                "transcription": r.get('transcription'),
                "ai_evaluation": r.get('ai_evaluation'),
                "quality_score": r.get('quality_score'),
                "passed": r.get('passed'),
                "concepts_identified": r.get('concepts_identified'),
                "created_at": r['created_at']
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

