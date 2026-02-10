from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseFileLoader(ABC):
    """Abstract base class for file loaders."""
    
    @abstractmethod
    def load(self, path: str) -> List[Document]:
        """Loads documents from the given path."""
        pass
