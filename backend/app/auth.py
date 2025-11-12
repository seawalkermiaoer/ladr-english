from __future__ import annotations

import os
from typing import Optional

from fastapi import Header, HTTPException


def _expected_token() -> Optional[str]:
    return os.getenv("WORD_TOKEN_SECRET")


async def require_bearer_token(authorization: Optional[str] = Header(default=None)) -> str:
    """Validate Authorization header and return token string.

    Rules:
    - Header must be present as: Authorization: Bearer <token>
    - If env WORD_TOKEN_SECRET is set, token must equal to it; otherwise any non-empty token is accepted.
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="invalid Authorization scheme")

    token = parts[1]
    if not token:
        raise HTTPException(status_code=401, detail="empty token")

    expected = _expected_token()
    if expected is not None and token != expected:
        raise HTTPException(status_code=401, detail="token invalid")

    return token

