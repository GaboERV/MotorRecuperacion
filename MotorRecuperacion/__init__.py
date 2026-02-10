from dotenv import load_dotenv
load_dotenv()

from .main import RecoveryEngine
from .database.config import get_db, init_db
from .config import config

def configure(database_url: str = None, upload_dir: str = None):
    """
    Configures the RAG system globally.
    Call this before using rag_client or creating new RAGSystem instances.
    """
    if database_url:
        config.database_url = database_url
    if upload_dir:
        config.upload_dir = upload_dir
        
    # Re-initialize database engine with new config
    if config.database_url:
        init_db()

def create_RecoveryEngine_client():
    """
    Factory function to create a new RAGSystem instance with its own database session.
    Ensures database is initialized.
    """
    # Auto-init if not done (and we have a URL)
    if config.database_url and not hasattr(config, '_db_initialized'):
         init_db()
         config._db_initialized = True

    db_session = next(get_db())
    return RecoveryEngine(db_session)

__all__ = ["RecoveryEngine", "create_RecoveryEngine_client", "configure"]
