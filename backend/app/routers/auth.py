from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth import require_bearer_token


router = APIRouter(prefix="/api", tags=["auth"])


@router.get("/verify")
async def verify(token: str = Depends(require_bearer_token)):
    return {"ok": True, "token": token}

