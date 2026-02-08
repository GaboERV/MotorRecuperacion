import logging
from typing import List
from langchain_core.documents import Document
from ..loaders import FileLoaderFactory

logger = logging.getLogger(__name__)

class FileManager:
    """
    Manages file retrieval and loading.
    """
    @staticmethod
    def load_documents(file_paths: List[str]) -> List[Document]:
        """
        Given a list of local file paths, loads them into Document objects.
        """
        documents = []

        for path in file_paths:
            try:
                # Load file content directly
                loader = FileLoaderFactory.get_loader(path)
                if loader:
                    docs = loader.load(path)
                    documents.extend(docs)
                else:
                    logger.warning(f"Formato no soportado para: {path}")
                    
            except Exception as e:
                logger.error(f"Error procesando {path}: {e}")
        
        return documents
