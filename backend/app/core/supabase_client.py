from typing import Optional, Any
import logging
from supabase import create_client, Client

from app.core.config import settings

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class SupabaseClient:
    """Supabase client wrapper for database operations."""
    
    def __init__(self):
        # Log the actual values being used
        logger.info(f"Initializing Supabase client with URL: {settings.SUPABASE_URL}")
        logger.info(f"Supabase anon key present: {settings.SUPABASE_ANON_KEY is not None}")
        if settings.SUPABASE_ANON_KEY:
            logger.info(f"Supabase anon key length: {len(settings.SUPABASE_ANON_KEY)}")
        
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        try:
            self.client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> Optional[Any]:
        """Verify token by checking if it matches the token column in the user table."""
        logger.info(f"Verifying token: {token[:10]}...")  # Log only first 10 characters for security
        try:
            # Check if any user has this token in their token column
            response = self.client.table("user").select("*").eq("token", token).execute()
            if response.data:
                user_data = response.data[0]
                user_id = user_data.get('id', 'unknown') if isinstance(user_data, dict) else getattr(user_data, 'id', 'unknown')
                current_level = user_data.get('current_level', 'unknown') if isinstance(user_data, dict) else getattr(user_data, 'current_level', 'unknown')
                logger.info(f"Token verified successfully for user ID: {user_id}, Current Level: {current_level}")
                return user_data
            logger.info("Token verification failed - invalid token")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            # Log more details about the error for debugging
            if hasattr(e, '__dict__'):
                logger.error(f"Exception attributes: {e.__dict__}")
            return None
