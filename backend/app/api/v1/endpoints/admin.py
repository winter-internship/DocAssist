from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from app.api import deps
from app.models.user import User, UserRole
from app.models.document import Document
from app.schemas.user import UserRead
from app.api.deps import get_current_admin_user

router = APIRouter()

@router.get("/metrics")
async def get_system_metrics(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get system metrics (admin only)
    """
    # Simple counts
    user_count = await db.scalar(text("SELECT count(*) FROM users"))
    doc_count = await db.scalar(text("SELECT count(*) FROM documents WHERE deleted_at IS NULL"))
    
    print(f"DEBUG: Admin metrics - Users: {user_count}, Docs: {doc_count}") # 로그 추가

    return {
        "users": user_count,
        "docs": doc_count,
        "queue": 0,
        "qaToday": 0
    }

@router.get("/users", response_model=List[UserRead])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get all users (admin only)
    """
    result = await db.execute(select(User).offset(skip).limit(limit).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return users

# Need a schema for document list in admin, probably same as DocumentRead or similar
from app.schemas.document import DocumentRead as DocumentSchema

@router.get("/documents", response_model=List[DocumentSchema])
async def get_all_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get all documents (admin only)
    """
    result = await db.execute(
        select(Document)
        .filter(Document.deleted_at == None)
        .offset(skip)
        .limit(limit)
        .order_by(Document.created_at.desc())
    )
    documents = result.scalars().all()
    return documents
