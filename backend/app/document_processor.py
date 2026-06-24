import os
import PyPDF2
import docx2txt
from PIL import Image
import pytesseract
from typing import List, Dict
import hashlib
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    @staticmethod
    def process_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise

    @staticmethod
    def process_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            logger.error(f"Error processing DOCX: {e}")
            raise

    @staticmethod
    def process_txt(file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error processing TXT: {e}")
            raise

    @staticmethod
    def process_image(file_path: str) -> str:
        """Extract text from image using OCR."""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise

    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """Extract text based on file type."""
        processors = {
            '.pdf': DocumentProcessor.process_pdf,
            '.docx': DocumentProcessor.process_docx,
            '.doc': DocumentProcessor.process_docx,
            '.txt': DocumentProcessor.process_txt,
            '.png': DocumentProcessor.process_image,
            '.jpg': DocumentProcessor.process_image,
            '.jpeg': DocumentProcessor.process_image,
        }
        
        processor = processors.get(file_type.lower())
        if not processor:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return processor(file_path)

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """Split text into overlapping chunks."""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if chunk_text.strip():
                chunks.append({
                    'content': chunk_text,
                    'metadata': {
                        'chunk_index': len(chunks),
                        'word_count': len(chunk_words),
                        'start_position': i,
                    }
                })
        
        return chunks

    @staticmethod
    def generate_file_hash(file_path: str) -> str:
        """Generate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
