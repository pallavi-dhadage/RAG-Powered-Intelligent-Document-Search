from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os

from app.database import get_db
from app.models import Document, DocumentCreate, DocumentResponse
from app.document_processor import DocumentProcessor
from app.rag_engine import rag_engine
from app.utils.file_handlers import FileHandler
from app.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    """Upload and process a document."""
    try:
        # Validate file
        valid, message = FileHandler.validate_file(file.filename, file.size)
        if not valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Save file
        file_path, original_name = FileHandler.save_file(file)
        
        # Extract file extension
        ext = os.path.splitext(original_name)[1].lower()
        
        # Extract text from document
        try:
            text = DocumentProcessor.extract_text(file_path, ext)
        except Exception as e:
            FileHandler.delete_file(file_path)
            raise HTTPException(status_code=400, detail=f"Error processing document: {str(e)}")
        
        # Create document record
        doc_data = DocumentCreate(
            filename=original_name,
            file_type=ext,
            file_size=file.size,
            title=title or original_name,
            description=description or ""
        )
        
        db_doc = Document(**doc_data.dict())
        db_doc.file_path = file_path
        
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        
        # Process and chunk document
        chunks = DocumentProcessor.chunk_text(
            text, 
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP
        )
        
        # Add to vector database
        rag_engine.add_documents(db_doc.id, chunks)
        
        logger.info(f"Document {original_name} processed successfully with {len(chunks)} chunks")
        
        return db_doc
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(db: Session = Depends(get_db)):
    """List all documents."""
    try:
        documents = db.query(Document).order_by(Document.created_at.desc()).all()
        return documents
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document."""
    try:
        db_doc = db.query(Document).filter(Document.id == document_id).first()
        if not db_doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from filesystem
        FileHandler.delete_file(db_doc.file_path)
        
        # Delete from vector database
        rag_engine.delete_document(document_id)
        
        # Delete from database
        db.delete(db_doc)
        db.commit()
        
        return {"message": f"Document {document_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stats")
async def get_stats():
    """Get vector database statistics."""
    try:
        stats = rag_engine.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
