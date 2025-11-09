from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import users, videos, progress, dashboard, contents, activities, activity_responses, dashboard_frontend
from app.config import UPLOAD_DIR, AUDIO_UPLOAD_DIR
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FeedBreak API",
    version="1.0.0",
    description="Backend API para FeedBreak - Educação através de vídeos curtos com E2E personalizados",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "FeedBreak API is running",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "FeedBreak API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    contents.router,
    prefix="/api/v1/contents",
    tags=["Contents"]
)

app.include_router(
    videos.router,
    prefix="/api/v1/videos",
    tags=["Videos"]
)

app.include_router(
    activities.router,
    prefix="/api/v1/activities",
    tags=["Activities"]
)

app.include_router(
    activity_responses.router,
    prefix="/api/v1/responses",
    tags=["Activity Responses"]
)

app.include_router(
    progress.router,
    prefix="/api/v1/progress",
    tags=["Progress"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    dashboard_frontend.router,
    prefix="/api/v1/dashboard-frontend",
    tags=["Dashboard Frontend"]
)

@app.on_event("startup")
async def startup_event():
    logger.info("FeedBreak API starting up...")
    logger.info("API documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FeedBreak API shutting down...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True, log_level="info")

