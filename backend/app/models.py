from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    title = Column(String(255))
    description = Column(Text)
    extra_metadata = Column(JSON)  # Changed from 'metadata' to 'extra_metadata'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    extra_metadata = Column(JSON)  # Changed from 'metadata' to 'extra_metadata'

# Pydantic models for API
class DocumentCreate(BaseModel):
    filename: str
    file_type: str
    file_size: int
    title: Optional[str] = None
    description: Optional[str] = None
    extra_metadata: Optional[dict] = None

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    title: Optional[str]
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    chunk_id: int
    document_id: int
    filename: str
    content: str
    score: float
    extra_metadata: Optional[dict]
