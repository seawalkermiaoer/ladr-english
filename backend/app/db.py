from __future__ import annotations

import os
import datetime as dt
from typing import Iterable, Optional, Tuple

from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()


class Word(Base):
    """SQLAlchemy ORM model for a vocabulary word.

    Attributes:
        id: Primary key.
        text: The vocabulary word (unique).
        definition: Optional definition or note.
        source: Optional source (e.g., article, URL, file).
        created_at: Creation timestamp.
        last_reviewed: Timestamp of the last review.
        review_count: Total number of reviews.
        easiness: Easiness factor (for spacing), defaults to 2.5.
        due_date: Next review due date.
    """

    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(256), unique=True, nullable=False, index=True)
    definition = Column(String(2048), nullable=True)
    source = Column(String(1024), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_reviewed = Column(DateTime, nullable=True)
    review_count = Column(Integer, nullable=False, default=0)
    easiness = Column(Float, nullable=False, default=2.5)
    due_date = Column(DateTime, nullable=True)


def _database_url() -> str:
    """Return database URL, prefer env var `WORD_DB_URL`.

    Defaults to a local SQLite file under `data/words.db` inside backend.
    """

    url = os.environ.get("WORD_DB_URL")
    if url:
        return url

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return f"sqlite:///{os.path.join(data_dir, 'words.db')}"


ENGINE = create_engine(_database_url(), echo=False, future=True)
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """Create tables if not exists."""

    Base.metadata.create_all(bind=ENGINE)


def override_database(url: str) -> None:
    """Override database engine/session with the given URL and re-create tables."""

    global ENGINE, SessionLocal
    ENGINE.dispose()
    ENGINE = create_engine(url, echo=False, future=True)
    SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)
    init_db()


def create_word(db: Session, text: str, definition: Optional[str], source: Optional[str]) -> Word:
    """Create a new word.

    Raises:
        ValueError: If the word already exists.
    """

    existing = db.query(Word).filter(Word.text == text).first()
    if existing:
        raise ValueError("word already exists")
    w = Word(text=text, definition=definition, source=source)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


def get_word(db: Session, word_id: int) -> Optional[Word]:
    """Get word by id."""

    return db.query(Word).filter(Word.id == word_id).first()


def get_word_by_text(db: Session, text: str) -> Optional[Word]:
    """Get word by text."""

    return db.query(Word).filter(Word.text == text).first()


def list_words(
    db: Session,
    q: Optional[str],
    skip: int,
    limit: int,
) -> Tuple[int, Iterable[Word]]:
    """List words with optional search and pagination.

    Returns total count and an iterable of result rows.
    """

    query = db.query(Word)
    if q:
        like = f"%{q}%"
        query = query.filter(Word.text.ilike(like))
    total = query.count()
    rows = query.order_by(Word.due_date.nulls_last(), Word.text).offset(skip).limit(limit).all()
    return total, rows


def update_word(
    db: Session,
    word_id: int,
    *,
    text: Optional[str] = None,
    definition: Optional[str] = None,
    source: Optional[str] = None,
) -> Optional[Word]:
    """Update word fields. Returns updated word or None if not found."""

    w = get_word(db, word_id)
    if not w:
        return None
    if text is not None:
        # Ensure uniqueness when renaming.
        exists = db.query(Word).filter(Word.text == text, Word.id != word_id).first()
        if exists:
            raise ValueError("word text already exists")
        w.text = text
    if definition is not None:
        w.definition = definition
    if source is not None:
        w.source = source
    db.commit()
    db.refresh(w)
    return w


def delete_word(db: Session, word_id: int) -> bool:
    """Delete by id. Returns True if deleted."""

    w = get_word(db, word_id)
    if not w:
        return False
    db.delete(w)
    db.commit()
    return True


def review_word(db: Session, word_id: int, quality: int) -> Optional[Word]:
    """Record a review with SM-2-like easiness update.

    Args:
        quality: 0–5. Lower means harder.
    """

    w = get_word(db, word_id)
    if not w:
        return None

    now = dt.datetime.now()
    w.last_reviewed = now
    w.review_count = (w.review_count or 0) + 1

    q = max(0, min(5, quality))
    e = w.easiness or 2.5
    e = max(1.3, e + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
    w.easiness = e

    interval_days = 1 if w.review_count == 1 else (6 if w.review_count == 2 else int((w.review_count - 1) * e))
    w.due_date = now + dt.timedelta(days=interval_days)

    db.commit()
    db.refresh(w)
    return w


def stats(db: Session) -> dict:
    """Return simple statistics for the word list."""

    total = db.query(Word).count()
    reviewed = db.query(Word).filter(Word.review_count > 0).count()
    due_today = db.query(Word).filter(Word.due_date <= dt.datetime.now()).count()
    return {"total": total, "reviewed": reviewed, "due_today": due_today}
