from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from .base import BaseFileLoader

class TextHandler(BaseFileLoader):
    def load(self, path: str) -> List[Document]:
        return TextLoader(path).load()
