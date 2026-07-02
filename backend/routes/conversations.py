from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from database.config import get_db
from database.models import Conversation
from backend.services.auth import get_current_user

router = APIRouter(prefix='/conversations')

class ConversationResponse(BaseModel):
    id: UUID
    title: str
    created_at: str

    class Config:
        orm_mode = True

@router.post("/", operation_id="create_conversation", status_code=status.HTTP_201_CREATED)
async def create_conversation(title: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    conversation = Conversation(
        id=str(uuid4()),
        user_id=current_user.id,
        title=title,
        created_at=datetime.utcnow()
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return {"message": "Conversation created successfully"}

@router.get("/", operation_id="list_conversations", response_model=List[ConversationResponse])
async def list_conversations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    return conversations