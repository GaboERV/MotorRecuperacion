from .main import RAGSystem, rag_client
from .database.config import get_db

def create_rag_client():
    """
    Factory function to create a new RAGSystem instance with its own database session.
    """
    db_session = next(get_db())
    return RAGSystem(db_session)

__all__ = ["RAGSystem", "rag_client", "create_rag_client"]
