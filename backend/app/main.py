from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, videos, progress, questions, answers, dashboard
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="FeedBreak API",
    version="1.0.0",
    description="Backend API para FeedBreak - Educação através de vídeos curtos com E2E personalizados",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (allow all origins for hackathon/MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "ok",
        "message": "FeedBreak API is running",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "FeedBreak API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Include routers
app.include_router(
    users.router,
    prefix="/api/v1/user",
    tags=["Users"]
)

app.include_router(
    videos.router,
    prefix="/api/v1/videos",
    tags=["Videos"]
)

app.include_router(
    progress.router,
    prefix="/api/v1/progress",
    tags=["Progress"]
)

app.include_router(
    questions.router,
    prefix="/api/v1/questions",
    tags=["Questions"]
)

app.include_router(
    answers.router,
    prefix="/api/v1/answer",
    tags=["Answers"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("FeedBreak API starting up...")
    logger.info("API documentation available at /docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FeedBreak API shutting down...")

# Main entry point for uvicorn
if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

