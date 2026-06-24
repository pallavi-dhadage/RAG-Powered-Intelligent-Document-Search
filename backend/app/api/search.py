from fastapi import APIRouter, HTTPException
from app.models import SearchQuery, SearchResult
from app.rag_engine import rag_engine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=list[SearchResult])
async def search_documents(search_query: SearchQuery):
    """Search for documents using RAG."""
    try:
        results = rag_engine.search(
            query=search_query.query,
            top_k=search_query.top_k
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'content': result['content'],
                'score': result['score'],
                'metadata': result['metadata'],
                'document_id': result['metadata']['document_id'],
                'chunk_id': result['metadata']['chunk_index']
            })
        
        logger.info(f"Search completed for query: {search_query.query[:50]}...")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
