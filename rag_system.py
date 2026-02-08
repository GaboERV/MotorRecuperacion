from typing import List, Optional
from sqlalchemy.orm import Session
from services.file_service import FileService
from managers import FileManager
from managers.rag_engine import process_and_query

class RAGSystem:
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
