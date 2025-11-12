import os
from typing import Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Obsidian Word GPT Backend"
    PROJECT_VERSION: str = "0.1.0"
    
    # Supabase settings
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY")
    
    # CORS settings
    CORS_ALLOWED_ORIGINS: Optional[str] = os.getenv("CORS_ALLOWED_ORIGINS")
    

settings = Settings()