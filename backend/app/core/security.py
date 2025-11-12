from __future__ import annotations

import logging
from typing import Optional

from fastapi import Header, HTTPException

from app.core.supabase_client import SupabaseClient

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


async def require_bearer_token(authorization: Optional[str] = Header(default=None)) -> str:
    """Validate Authorization header and return token string.
    
    Rules:
    - Header must be present as: Authorization: Bearer <token>
    - Token must exist in the Supabase user table
    """
    
    if not authorization:
        logger.warning("Missing Authorization header")
        raise HTTPException(status_code=401, detail="missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning(f"Invalid Authorization scheme: {authorization}")
        raise HTTPException(status_code=401, detail="invalid Authorization scheme")

    token = parts[1]
    if not token:
        logger.warning("Empty token provided")
        raise HTTPException(status_code=401, detail="empty token")

    # Verify token against Supabase user table
    try:
        logger.info(f"Verifying token: {token[:10]}...")  # Log only first 10 characters for security
        supabase_client = SupabaseClient()
        user_data = supabase_client.verify_token(token)
        if not user_data:
            logger.warning("Invalid token provided")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Token verified successfully")
    except HTTPException:
        # Re-raise HTTP exceptions without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Error verifying token: {str(e)}")

    return token
