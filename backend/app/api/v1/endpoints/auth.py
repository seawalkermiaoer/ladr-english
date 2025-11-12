from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from app.core.security import require_bearer_token
from app.services.user_service import UserService
from app.schemas.user import TokenVerificationOut

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


router = APIRouter(tags=["auth"])


@router.get("/verify", response_model=TokenVerificationOut)
async def verify_token(token: str = Depends(require_bearer_token)):
    """Verify the authentication token against Supabase user table."""
    logger.info(f"Verifying token: {token[:10]}...")  # Log only first 10 characters for security
    try:
        # Initialize user service
        user_service = UserService()
        
        # Verify token by checking if it corresponds to a valid user
        user = user_service.verify_user_token(token)
        
        if user:
            logger.info(f"Token verified successfully for user ID: {user.id}, Current Level: {user.current_level}")
            return TokenVerificationOut(
                ok=True,
                token=token,
                user=user
            )
        else:
            logger.warning("Invalid token provided")
            raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException:
        # Re-raise HTTP exceptions (like 401) without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error verifying token: {str(e)}")