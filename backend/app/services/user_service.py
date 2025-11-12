from typing import Optional, List, Any
import logging
from app.core.supabase_client import SupabaseClient
from app.schemas.user import UserOut

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class UserService:
    """Service class for user-related operations with Supabase."""
    
    def __init__(self):
        self.supabase_client = SupabaseClient()
    
    def verify_user_token(self, token: str) -> Optional[UserOut]:
        """Verify user token and return user information."""
        logger.info(f"Verifying token: {token[:10]}...")  # Log only first 10 characters for security
        user_data: Any = self.supabase_client.verify_token(token)
        if user_data:
            # Handle both dict and object cases
            if isinstance(user_data, dict):
                user_id = user_data.get('id', 'unknown')
                current_level = user_data.get('current_level', 'unknown')
                logger.info(f"Token verified successfully for user ID: {user_id}, Current Level: {current_level}")
                return UserOut(
                    id=str(user_data.get("id", "")),
                    created_at=user_data.get("created_at"),
                    current_level=user_data.get("current_level")
                )
            else:
                # If it's an object, try to access attributes
                user_id = getattr(user_data, "id", "unknown")
                current_level = getattr(user_data, "current_level", "unknown")
                logger.info(f"Token verified successfully for user ID: {user_id}, Current Level: {current_level}")
                return UserOut(
                    id=str(user_id),
                    created_at=getattr(user_data, "created_at", None),
                    current_level=getattr(user_data, "current_level", None)
                )
        logger.info("Token verification failed - invalid token")
        return None
