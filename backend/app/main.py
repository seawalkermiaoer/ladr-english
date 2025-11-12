from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routers.words import router as words_router
from app.routers.auth import router as auth_router


def _allowed_origins() -> list[str]:
    """Return allowed CORS origins. Defaults to localhost for dev."""

    origins = os.environ.get("WORD_ALLOWED_ORIGINS")
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


app = FastAPI(title="Obsidian Word GPT Backend", version="0.1.0")

# Initialize database tables.
init_db()

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


app.include_router(words_router)
app.include_router(auth_router)