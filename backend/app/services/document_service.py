import os
import shutil
import uuid
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)
from uuid import UUID
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sa_update
from sqlalchemy.orm import selectinload

from app.models.document import Document, DocStatus, DocumentJob, JobStatus, DocumentEmbedding, DocumentAnalysis, GlossaryTerm
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services.document_processor import processor

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get(db: AsyncSession, id: UUID) -> Optional[Document]:
    # 분석 및 용어집 관계를 즉시 로드 (Eager load)
    result = await db.execute(
        select(Document)
        .options(selectinload(Document.analysis), selectinload(Document.glossary_terms))
        .filter(Document.id == id, Document.deleted_at == None)
    )
    return result.scalars().first()

async def get_multi_by_user(
    db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100
) -> List[Document]:
    result = await db.execute(
        select(Document)
        .filter(Document.user_id == user_id, Document.deleted_at == None)
        .offset(skip)
        .limit(limit)
        .order_by(Document.created_at.desc())
    )
    return result.scalars().all()

async def get_authorized(db: AsyncSession, id: UUID, user_id: UUID) -> Optional[Document]:
    """Retrieve document only if it belongs to the user."""
    doc = await get(db, id)
    if doc and doc.user_id == user_id:
        return doc
    return None

async def create_with_file(
    db: AsyncSession, user_id: UUID, file: UploadFile
) -> Document:
    # 1. 파일을 로컬에 저장
    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    
    # 참고: 비동기 함수 내 블로킹 I/O
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. DB 레코드 생성
    file_size = os.path.getsize(file_path)
    
    db_obj = Document(
        user_id=user_id,
        title=file.filename,
        original_filename=file.filename,
        s3_key=file_path, # 현재는 로컬 경로 저장
        file_type=file_ext.replace(".", "").upper(), # 예: PDF
        file_size=file_size,
        status=DocStatus.QUEUED,
        meta_data={}
    )
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj

async def update(
    db: AsyncSession, db_obj: Document, obj_in: DocumentUpdate
) -> Document:
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove(db: AsyncSession, id: UUID) -> Optional[Document]:
    # 소프트 삭제 (Soft delete)
    result = await db.execute(select(Document).filter(Document.id == id))
    db_obj = result.scalars().first()
    if db_obj:
        db_obj.deleted_at = datetime.utcnow()
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
    return db_obj

async def process_document_background(db: AsyncSession, document_id: UUID):
    """
    문서 처리 백그라운드 태스크: 텍스트 추출 -> 청킹 -> 임베딩 -> 저장 -> 분석
    """
    # 1. 문서 조회
    result = await db.execute(select(Document).filter(Document.id == document_id))
    doc = result.scalars().first()
    
    if not doc:
        print(f"Document {document_id} not found for processing")
        return

    # 작업 기록 생성 (Create Job Record)
    job = DocumentJob(
        document_id=document_id,
        status=JobStatus.RUNNING,
        started_at=datetime.utcnow()
    )
    db.add(job)
    
    try:
        # 문서 상태 업데이트 (Update Document Status)
        doc.status = DocStatus.PROCESSING
        db.add(doc)
        await db.commit()

        # 2. 텍스트 추출 (Extract Text)
        text = processor.extract_text(doc.s3_key, doc.file_type)
        if not text:
            raise Exception("No text extracted or empty file")

        # 3. 청킹 (Chunk)
        chunks = processor.chunk_text(text)
        
        # 4. 임베딩 생성 (Embed)
        embeddings = await processor.create_embeddings(chunks)
        
        # 5. 임베딩 저장 (Save Embeddings)
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            db_emb = DocumentEmbedding(
                document_id=document_id,
                chunk_index=i,
                chunk_content=chunk,
                embedding=embedding
            )
            db.add(db_emb)
            
            # 6. 문서 분석 (GPT) - Analyze Document
        logger.info(f"Analyzing document {document_id} with GPT...")
        analysis_result = await processor.analyze_document(text)
        
        if analysis_result:
            # 분석 결과 저장 (Save Analysis)
            db_analysis = DocumentAnalysis(
                document_id=document_id,
                summary=analysis_result.get("summary"),
                paragraphs=analysis_result.get("paragraphs", []),
                rules=analysis_result.get("rules", [])
            )
            db.add(db_analysis)
            
            # 용어집 저장 (Save Glossary Terms)
            terms = analysis_result.get("terms", [])
            for t in terms:
                db_term = GlossaryTerm(
                    document_id=document_id,
                    term=t.get("term"),
                    definition=t.get("definition"),
                    tags=[],
                    complexity_level=1
                )
                db.add(db_term)
        
        # 상태를 완료(DONE)로 업데이트
        doc.status = DocStatus.DONE
        job.status = JobStatus.COMPLETED
        job.finished_at = datetime.utcnow()
        job.result_data = {"chunks": len(chunks), "analysis": bool(analysis_result)}
        
        db.add(doc)
        db.add(job)
        await db.commit()
        logger.info(f"Document {document_id} processed successfully.")

    except Exception as e:
        logger.error(f"Processing failed for document {document_id}: {e}")
        await db.rollback()
        
        doc.status = DocStatus.FAILED
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        job.finished_at = datetime.utcnow()
        
        db.add(doc)
        db.add(job)
        await db.commit()
