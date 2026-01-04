from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from app.models.chat import ChatSession, ChatMessage, ChatRole
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate
from app.services.rag_service import rag_service

async def create_session(
    db: AsyncSession, user_id: UUID, obj_in: ChatSessionCreate
) -> ChatSession:
    db_obj = ChatSession(
        user_id=user_id,
        document_id=obj_in.document_id,
        title=obj_in.title or "New Chat"
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_session(db: AsyncSession, session_id: UUID) -> Optional[ChatSession]:
    result = await db.execute(select(ChatSession).filter(ChatSession.id == session_id))
    return result.scalars().first()

async def get_user_sessions(
    db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 50
) -> List[ChatSession]:
    result = await db.execute(
        select(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(desc(ChatSession.updated_at))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_message(
    db: AsyncSession, session_id: UUID, obj_in: ChatMessageCreate
) -> ChatMessage:
    db_obj = ChatMessage(
        session_id=session_id,
        role=obj_in.role,
        content=obj_in.content,
        citations=obj_in.citations or []
    )
    db.add(db_obj)
    
    # Update session updated_at
    session = await get_session(db, session_id)
    if session:
        session.updated_at = datetime.utcnow()
        db.add(session)
        
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_messages(
    db: AsyncSession, session_id: UUID, skip: int = 0, limit: int = 100
) -> List[ChatMessage]:
    result = await db.execute(
        select(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def process_question(
    db: AsyncSession,
    session_id: UUID,
    question: str,
    user_settings: dict = None
) -> ChatMessage:
    """
    Process a user question: save message, retrieve context, generate response, save response.
    """
    # 1. Save User Message
    user_msg_in = ChatMessageCreate(role=ChatRole.USER, content=question)
    await create_message(db, session_id, user_msg_in)

    # 2. Get Context History
    previous_messages = await get_messages(db, session_id, limit=20)
    
    # Helper to safe access role value
    def get_role_value(role):
        return role.value if hasattr(role, 'value') else role

    llm_messages = [{"role": get_role_value(msg.role), "content": msg.content} for msg in previous_messages]
    
    # 3. Get Session Info (for document_id)
    session = await get_session(db, session_id)
    
    # 4. RAG Service Call
    response_in = await rag_service.get_chat_completion(
        db=db,
        query=question,
        messages=llm_messages,
        document_id=session.document_id if session else None,
        user_settings=user_settings
    )
    
    # 5. Save Assistant Message
    return await create_message(db, session_id, response_in)
