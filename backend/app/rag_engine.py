import logging
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from app.config import settings
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self):
        # Fixed embedding dimension
        self.embedding_dim = 384
        self.vectorizer = TfidfVectorizer(max_features=self.embedding_dim)
        self._is_fitted = False
        
        # Ensure clean start
        self._clean_chromadb()
        
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self._get_or_create_collection()
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def _clean_chromadb(self):
        """Clean up ChromaDB data if exists."""
        chroma_path = settings.CHROMA_PERSIST_DIR
        if os.path.exists(chroma_path):
            # Check if there's data
            if os.path.exists(os.path.join(chroma_path, "chroma.sqlite3")):
                logger.warning("Existing ChromaDB data found. Starting fresh.")
                # Backup and remove
                backup_path = chroma_path + "_backup"
                if os.path.exists(backup_path):
                    shutil.rmtree(backup_path)
                shutil.move(chroma_path, backup_path)
                logger.info(f"Backed up old data to {backup_path}")
        
        # Create fresh directory
        os.makedirs(chroma_path, exist_ok=True)

    def _get_or_create_collection(self):
        try:
            # Try to get existing collection
            collection = self.chroma_client.get_collection(settings.COLLECTION_NAME)
            logger.info(f"Collection '{settings.COLLECTION_NAME}' loaded.")
            return collection
        except:
            # Create new collection with proper dimension
            collection = self.chroma_client.create_collection(
                name=settings.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Collection '{settings.COLLECTION_NAME}' created with dimension {self.embedding_dim}.")
            return collection

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings with fixed dimension."""
        # Fit vectorizer if not fitted
        if not self._is_fitted:
            self.vectorizer.fit(texts)
            self._is_fitted = True
            logger.info(f"Vectorizer fitted with dimension: {self.embedding_dim}")
        
        # Transform texts
        embeddings = self.vectorizer.transform(texts).toarray()
        
        # Ensure correct dimension
        if embeddings.shape[1] < self.embedding_dim:
            # Pad with zeros
            padded = np.zeros((embeddings.shape[0], self.embedding_dim))
            padded[:, :embeddings.shape[1]] = embeddings
            embeddings = padded
        elif embeddings.shape[1] > self.embedding_dim:
            # Truncate
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
            ids = [f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))]
            
            # Generate embeddings
            embeddings = self.generate_embeddings(texts)
            
            # Add to collection
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(chunks)} chunks for document {document_id}")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        try:
            # Check if collection has data
            if self.collection.count() == 0:
                return []
            
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])[0]
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.collection.count()),
                include=['documents', 'metadatas', 'distances']
            )
            
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    search_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i],
                        'score': 1 - results['distances'][0][i]
                    })
            return search_results
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise

    def delete_document(self, document_id: int) -> None:
        try:
            self.collection.delete(where={"document_id": document_id})
            logger.info(f"Deleted document {document_id} from vector DB")
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise

    def get_stats(self) -> Dict:
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': settings.COLLECTION_NAME,
                'embedding_model': f'TF-IDF (dim={self.embedding_dim})'
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            raise

rag_engine = RAGEngine()
logger.info("RAG Engine created successfully with clean database")
