from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from .base import BaseFileLoader

class PdfHandler(BaseFileLoader):
    def load(self, path: str) -> List[Document]:
        return PyPDFLoader(path).load()
