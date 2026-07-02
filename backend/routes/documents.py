from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.config import get_db
from database.models import Document
from backend.services.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/documents")

class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    status: str
    chunk_count: int
    created_at: str

    class Config:
        orm_mode = True

@router.post("/upload", operation_id="upload_document", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    document = Document(
        id=str(uuid4()),
        user_id=current_user.id,
        filename=file.filename,
        status="uploaded",
        chunk_count=0,
        created_at=datetime.utcnow()
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return {"message": "Document uploaded successfully"}

@router.get("/", operation_id="list_documents", response_model=List[DocumentResponse])
async def list_documents(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@router.delete("/{id}", operation_id="delete_document", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    document = db.query(Document).filter(Document.id == str(id), Document.user_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}