from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from config import EMBEDDING_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_K

# Initialize embeddings globally to reuse the model
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def process_and_query(documents: List[Document], query: str) -> List[str]:
    """
    Processes loaded documents, performs a query, and cleans up the temporary vector store.
    
    Args:
        documents: List of pre-loaded Document objects.
        query: The query string to search for.
        
    Returns:
        List of result strings (page content).
    """
    if not documents:
        return ["No documents to process."]

    # 1. Splitter
    text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    splits = text_splitter.split_documents(documents)

    if not splits:
        return ["Documents empty after processing."]

    # 2. Temporary Vectorstore
    # Note: Chroma() allows passing a persistent directory, but without it, it's ephemeral/in-memory
    # However, to be extra safe with "cleanup", we track IDs.
    vectorstore = Chroma(embedding_function=embeddings, collection_name="temp_collection")
    ids = vectorstore.add_documents(splits)
    
    try:
        # 3. Query
        results = vectorstore.similarity_search(query, k=RETRIEVER_K)
        responses = [doc.page_content for doc in results]
    finally:
        # 4. Cleanup
        if ids:
            vectorstore.delete(ids=ids)
            
    return responses
