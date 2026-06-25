import logging
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self):
        self.embedding_dim = 384
        self.vectorizer = TfidfVectorizer(max_features=self.embedding_dim)
        self._is_fitted = False
        self.chunks = []
        self.metadatas = []
        self.documents = {}
        
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self._is_fitted:
            if texts:
                self.vectorizer.fit(texts)
                self._is_fitted = True
                logger.info(f"Vectorizer fitted with dimension: {self.embedding_dim}")
            else:
                return []
        
        if not self._is_fitted:
            return []
            
        embeddings = self.vectorizer.transform(texts).toarray()
        
        # Ensure correct dimension
        if embeddings.shape[1] < self.embedding_dim:
            padded = np.zeros((embeddings.shape[0], self.embedding_dim))
            padded[:, :embeddings.shape[1]] = embeddings
            embeddings = padded
        elif embeddings.shape[1] > self.embedding_dim:
            embeddings = embeddings[:, :self.embedding_dim]
        
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1
        embeddings = embeddings / norms
        
        return embeddings.tolist()

    def add_documents(self, document_id: int, chunks: List[Dict]) -> None:
        try:
            texts = [chunk['content'] for chunk in chunks]
            metadatas = [
                {
                    'document_id': document_id,
                    'chunk_index': chunk['metadata']['chunk_index'],
                    **chunk['metadata']
                }
                for chunk in chunks
            ]
            
            # Store chunks
            self.chunks.extend(texts)
            self.metadatas.extend(metadatas)
            
            # Store by document
            if document_id not in self.documents:
                self.documents[document_id] = []
            self.documents[document_id].extend(texts)
            
            # Refit vectorizer with all chunks
            if self.chunks:
                self._is_fitted = False
                self.vectorizer.fit(self.chunks)
                self._is_fitted = True
            
            logger.info(f"Added {len(chunks)} chunks for document {document_id}. Total chunks: {len(self.chunks)}")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        try:
            if not self.chunks:
                return []
            
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])[0]
            
            # Generate embeddings for all chunks
            all_embeddings = self.generate_embeddings(self.chunks)
            
            # Calculate similarities
            similarities = []
            for emb in all_embeddings:
                sim = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb) + 1e-10)
                similarities.append(sim)
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                results.append({
                    'content': self.chunks[idx],
                    'metadata': self.metadatas[idx],
                    'score': float(similarities[idx])
                })
            
            return results
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise

    def delete_document(self, document_id: int) -> None:
        try:
            # Remove chunks for this document
            indices_to_remove = []
            for i, meta in enumerate(self.metadatas):
                if meta['document_id'] == document_id:
                    indices_to_remove.append(i)
            
            if indices_to_remove:
                # Remove in reverse order
                for idx in sorted(indices_to_remove, reverse=True):
                    del self.chunks[idx]
                    del self.metadatas[idx]
                
                # Refit vectorizer
                if self.chunks:
                    self._is_fitted = False
                    self.vectorizer.fit(self.chunks)
                    self._is_fitted = True
                
            self.documents.pop(document_id, None)
            logger.info(f"Deleted document {document_id}")
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise

    def get_stats(self) -> Dict:
        try:
            return {
                'total_chunks': len(self.chunks),
                'total_documents': len(self.documents),
                'embedding_model': 'TF-IDF (in-memory)',
                'embedding_dim': self.embedding_dim
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            raise

rag_engine = RAGEngine()
logger.info("RAG Engine created successfully (in-memory TF-IDF)")
