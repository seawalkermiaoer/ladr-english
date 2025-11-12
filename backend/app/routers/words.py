from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import db
from app.models import WordCreate, WordUpdate, WordOut, WordListOut, ReviewIn, StatsOut


router = APIRouter(prefix="/api", tags=["words"])


def get_db() -> Session:
    """Yield a DB session for request lifetime."""

    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/words", response_model=WordOut)
def create_word(payload: WordCreate, session: Session = Depends(get_db)):
    try:
        w = db.create_word(session, payload.text.strip(), payload.definition, payload.source)
        return WordOut.model_validate(w)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/words", response_model=WordListOut)
def list_words(
    q: Optional[str] = Query(default=None, description="Search keyword in text"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_db),
):
    total, items = db.list_words(session, q, skip, limit)
    return WordListOut(total=total, items=[WordOut.model_validate(w) for w in items])


@router.get("/words/{word_id}", response_model=WordOut)
def get_word(word_id: int, session: Session = Depends(get_db)):
    w = db.get_word(session, word_id)
    if not w:
        raise HTTPException(status_code=404, detail="word not found")
    return WordOut.model_validate(w)


@router.put("/words/{word_id}", response_model=WordOut)
def update_word(word_id: int, payload: WordUpdate, session: Session = Depends(get_db)):
    try:
        w = db.update_word(
            session,
            word_id,
            text=payload.text.strip() if payload.text else None,
            definition=payload.definition,
            source=payload.source,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not w:
        raise HTTPException(status_code=404, detail="word not found")
    return WordOut.model_validate(w)


@router.delete("/words/{word_id}")
def delete_word(word_id: int, session: Session = Depends(get_db)):
    ok = db.delete_word(session, word_id)
    if not ok:
        raise HTTPException(status_code=404, detail="word not found")
    return {"ok": True}


@router.post("/words/{word_id}/review", response_model=WordOut)
def review_word(word_id: int, payload: ReviewIn, session: Session = Depends(get_db)):
    w = db.review_word(session, word_id, payload.quality)
    if not w:
        raise HTTPException(status_code=404, detail="word not found")
    return WordOut.model_validate(w)


@router.get("/stats", response_model=StatsOut)
def get_stats(session: Session = Depends(get_db)):
    return StatsOut(**db.stats(session))

