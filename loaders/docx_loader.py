from typing import List
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document
from .base import BaseFileLoader

class DocxHandler(BaseFileLoader):
    def load(self, path: str) -> List[Document]:
        return Docx2txtLoader(path).load()
