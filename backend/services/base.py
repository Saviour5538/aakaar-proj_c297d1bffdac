from typing import Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

T = TypeVar("T")  # Generic type for SQLAlchemy models

class BaseService:
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> T:
        try:
            obj = self.model(**obj_in)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get(self, db: Session, id: str) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session) -> List[T]:
        return db.query(self.model).all()

    def delete(self, db: Session, id: str) -> None:
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
            if obj:
                db.delete(obj)
                db.commit()
            else:
                raise HTTPException(status_code=404, detail="Object not found")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))