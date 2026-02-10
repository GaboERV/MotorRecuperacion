import os

class RecoveryEngineConfig:
    """
    Configuration singleton for the RAG system.
    """
    _instance = None

    def __init__(self):
        self.database_url = None
        self.upload_dir = os.path.join(os.getcwd(), "uploads")
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.retriever_k = 3

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# Global configuration instance
config = RecoveryEngineConfig.get_instance()

# Re-export variables for backward compatibility (they will be properties or just access the config object)
# Ideally, code should use config.database_url, etc.
DATABASE_URL = config.database_url
UPLOAD_DIR = config.upload_dir
EMBEDDING_MODEL_NAME = config.embedding_model_name
CHUNK_SIZE = config.chunk_size
CHUNK_OVERLAP = config.chunk_overlap
RETRIEVER_K = config.retriever_k
