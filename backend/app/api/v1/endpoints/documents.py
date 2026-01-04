import os
from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.document import DocumentRead, DocumentUpdate, DocumentWithAnalysis
from app.models.user import User
from app.services import document_service
from app.db.session import SessionLocal

router = APIRouter()

async def run_document_processing(document_id: UUID):
    async with SessionLocal() as db:
        await document_service.process_document_background(db, document_id)

async def _get_doc_or_404(db: AsyncSession, document_id: UUID, user: User):
    """Helper to retrieve authorized document or raise 404."""
    doc = await document_service.get_authorized(db, document_id, user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/upload", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")
    
    # 파일 저장 및 DB 항목 생성
    document = await document_service.create_with_file(db, current_user.id, file)
    
    # 문서 처리를 위한 백그라운드 태스크 추가 (OCR, 임베딩, 분석)
    background_tasks.add_task(run_document_processing, document.id)
    
    return document

@router.get("/", response_model=List[DocumentRead])
async def read_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    documents = await document_service.get_multi_by_user(db, current_user.id, skip=skip, limit=limit)
    return documents

@router.get("/{document_id}", response_model=DocumentWithAnalysis)
async def read_document(
    document_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    return await _get_doc_or_404(db, document_id, current_user)

@router.patch("/{document_id}", response_model=DocumentRead)
async def update_document(
    document_id: UUID,
    document_in: DocumentUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    document = await _get_doc_or_404(db, document_id, current_user)
    document = await document_service.update(db, document, document_in)
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> None:
    # 존재 여부 및 소유권 확인
    await _get_doc_or_404(db, document_id, current_user)
    await document_service.remove(db, document_id)
    return
