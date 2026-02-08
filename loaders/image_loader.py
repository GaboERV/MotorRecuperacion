from typing import List
from langchain_community.document_loaders import UnstructuredImageLoader
from langchain_core.documents import Document
from .base import BaseFileLoader

class ImageHandler(BaseFileLoader):
    def load(self, path: str) -> List[Document]:
        return UnstructuredImageLoader(path).load()
