import os
import shutil
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from .database.config import get_db, Base, engine
from .services.file_service import FileService
from .managers import FileManager
from .managers.rag_engine import process_and_query

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RecoveryEngine:
    """
    Facade for the RAG system.
    Encapsulates database operations, file management, and the RAG processing pipeline.
    """
    def __init__(self, db: Session):
        self.db = db
        self.file_service = FileService(db)

    def upload(self, user_email: str, filename: str, data: bytes) -> str:
        """
        Uploads a file for a user given filename and bytes.
        """
        try:
            file_record = self.file_service.upload_file(user_email, filename, data)
            return f"File '{file_record.filename}' uploaded successfully."
        except Exception as e:
            return f"Upload failed: {str(e)}"

    def ask(self, user_email: str, filenames: List[str], question: str) -> List[str]:
        """
        Orchestrates the query process:
        1. Validate user and files.
        2. Load documents.
        3. Process and query.
        """
        try:
            # 1. Validation
            valid_paths = self.file_service.get_validated_file_paths(user_email, filenames)
            
            if not valid_paths:
                return ["No valid files found for the requested criteria."]

            # 2. Loading
            docs = FileManager.load_documents(valid_paths)
            
            if not docs:
                return ["Failed to load content from the validated files."]

            # 3. Processing & Querying
            return process_and_query(docs, question)

        except Exception as e:
            return [f"An error occurred during query: {str(e)}"]

    def list_files(self, user_email: str) -> List[str]:
        """
        Returns list of files for the user.
        """
        return self.file_service.list_files(user_email)

    def delete(self, user_email: str, filename: str) -> str:
        """
        Deletes a file.
        """
        success = self.file_service.delete_file(user_email, filename)
        if success:
            return f"File '{filename}' deleted successfully."
        return f"Failed to delete '{filename}'. File not found or user does not exist."

# --- Exportable Instance ---
# --- Exportable Instance ---
try:
    # Attempt strict auto-initialization from environment if configured
    # This preserves standalone behavior (python -m MotorRecuperacion.main)
    # while allowing library usage to skip this if env vars aren't present
    if not engine: 
        # Check if we have env vars to auto-configure (standalone mode)
        db_url = os.environ.get("DATABASE_URL")
        # Fallback to constructing from parts if DATABASE_URL not set but parts are
        if not db_url and os.environ.get("DB_USER"):
             db_user = os.environ.get("DB_USER")
             db_pass = os.environ.get("DB_PASSWORD")
             db_host = os.environ.get("DB_HOST")
             db_name = os.environ.get("DB_NAME")
             db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
        
        if db_url:
             from . import configure
             configure(database_url=db_url)

    if engine:
        # Ensure database tables exist
        Base.metadata.create_all(bind=engine)
        
        # Create a default session and RAG instance
        _db_session = next(get_db())
        rag_client = RecoveryEngine(_db_session)
        logger.info("RAGSystem initialized and ready for export as 'rag_client'.")
    else:
        rag_client = None
        logger.info("RAGSystem awaiting configuration. Call 'configure(database_url=...)'")

except Exception as e:
    logger.error(f"Failed to initialize RAGSystem: {e}")
    rag_client = None

__all__ = ["RecoveryEngine", "rag_client"]
