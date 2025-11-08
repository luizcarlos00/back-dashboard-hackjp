import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase Configuration (for Storage only)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

# Initialize Supabase client (only for Storage)
supabase_storage: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Database Configuration (SQLAlchemy)
DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")

if not DATABASE_URL and not SUPABASE_DB_PASSWORD:
    raise ValueError("DATABASE_URL or SUPABASE_DB_PASSWORD must be set in environment variables")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set in environment variables")

# Server Configuration
PORT = int(os.getenv("PORT", 8000))

