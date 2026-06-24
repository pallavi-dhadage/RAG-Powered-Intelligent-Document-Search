import os
import shutil
from typing import Tuple
from datetime import datetime
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class FileHandler:
    @staticmethod
    def validate_file(filename: str, size: int) -> Tuple[bool, str]:
        """Validate file before upload."""
        # Check file size
        if size > settings.MAX_FILE_SIZE:
            return False, f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        
        # Check file extension
        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            return False, f"File type not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        
        return True, ""

    @staticmethod
    def save_file(uploaded_file, upload_dir: str = "uploads") -> Tuple[str, str]:
        """Save uploaded file and return file path."""
        try:
            # Create upload directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = uploaded_file.filename
            name, ext = os.path.splitext(original_name)
            safe_filename = f"{name}_{timestamp}{ext}"
            
            file_path = os.path.join(upload_dir, safe_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(uploaded_file.file, buffer)
            
            return file_path, original_name
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete file from filesystem."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
