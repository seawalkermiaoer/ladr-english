from typing import Optional, List, Any
from sqlalchemy.orm import Session


class BaseRepository:
    """Base repository class with common database operations."""

    def __init__(self, model: Any):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[Any]:
        """Get a record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[Any]:
        """List records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: Any) -> Any:
        """Create a new record."""
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Any, obj_in: Any) -> Any:
        """Update an existing record."""
        obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> bool:
        """Remove a record by ID."""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False