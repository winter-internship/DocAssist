from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from app.models.document import DocStatus, JobStatus

# Shared properties
class DocumentBase(BaseModel):
    title: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    status: Optional[DocStatus] = DocStatus.QUEUED
    meta_data: Optional[Dict[str, Any]] = None

# Properties to receive on document creation
class DocumentCreate(DocumentBase):
    title: str
    original_filename: str
    s3_key: str
    file_type: str
    file_size: int

# Properties to receive on document update
class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[DocStatus] = None
    meta_data: Optional[Dict[str, Any]] = None

# Properties shared by models stored in DB
class DocumentInDBBase(DocumentBase):
    id: UUID
    user_id: UUID
    original_filename: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Properties to return to client
class DocumentRead(DocumentInDBBase):
    pass

# Document Analysis Result Schema
class DocumentAnalysisRead(BaseModel):
    id: UUID
    document_id: UUID
    summary: Optional[str] = None
    paragraphs: List[Dict[str, Any]] = []
    rules: List[Dict[str, Any]] = []
    created_at: datetime

    class Config:
        from_attributes = True

class GlossaryTermRead(BaseModel):
    id: UUID
    term: str
    definition: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Extended Document Read with Analysis (optional)
class DocumentWithAnalysis(DocumentRead):
    analysis: Optional[DocumentAnalysisRead] = None
    glossary_terms: List[GlossaryTermRead] = []
