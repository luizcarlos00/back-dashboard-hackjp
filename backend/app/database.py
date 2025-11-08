from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback: construct from individual parts if DATABASE_URL not set
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD", "")
    
    if SUPABASE_URL and SUPABASE_DB_PASSWORD:
        # Extract host from Supabase URL
        host = SUPABASE_URL.replace("https://", "").replace("http://", "")
        db_host = f"db.{host}"
        DATABASE_URL = f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@{db_host}:5432/postgres"

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL or (SUPABASE_URL + SUPABASE_DB_PASSWORD) must be set in environment variables"
    )

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function to get database session.
    Use in FastAPI endpoints with Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
