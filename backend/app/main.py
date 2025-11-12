from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings
from app.api.v1.api import router as api_v1_router


def _allowed_origins() -> list[str]:
    """Return allowed CORS origins. Defaults to localhost for dev."""

    origins = settings.CORS_ALLOWED_ORIGINS
    if origins:
        return [o.strip() for o in origins.split(",") if o.strip()]
    return [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "capacitor://localhost",
        "ionic://localhost",
        "app://obsidian.md",  # Add Obsidian app origin
    ]


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# CORS for local development with Obsidian/electron-like environments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(api_v1_router)