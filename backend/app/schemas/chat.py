from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.models.chat import ChatRole

# Message Schemas
class ChatMessageBase(BaseModel):
    role: ChatRole
    content: str
    citations: Optional[List[Dict[str, Any]]] = []

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageRead(ChatMessageBase):
    id: UUID
    session_id: UUID
    created_at: datetime
    model_name: Optional[str] = None

    class Config:
        from_attributes = True

# Session Schemas
class ChatSessionBase(BaseModel):
    title: Optional[str] = None
    document_id: Optional[UUID] = None

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionRead(ChatSessionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    # Optional: Include last message or messages list
    # messages: List[ChatMessageRead] = []

    class Config:
        from_attributes = True

# Request Schema for Asking Question
class ChatQuestion(BaseModel):
    question: str
    model: str = "gpt-4o"


