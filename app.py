import os
import shutil
import logging
from database.config import get_db, Base, engine
from rag_system import RAGSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Setup
    email = "gaboe@example.com"
    dummy_file = "solid_principle.txt"
    
    # Create a local dummy file
    with open(dummy_file, "w") as f:
        f.write("SOLID principles ensure scalable and maintainable code. Single Responsibility is key.")

    # Initialize System with DB Session
    db = next(get_db())
    rag = RAGSystem(db)

    try:
        # 1. Upload
        logger.info(f"--- Uploading {dummy_file} ---")
        with open(dummy_file, "rb") as f:
            data = f.read()
        message = rag.upload(email, dummy_file, data)
        logger.info(message)

        # 2. List Files
        logger.info("--- Listing Files ---")
        files = rag.list_files(email)
        logger.info(f"User files: {files}")

        # 3. Ask Question
        logger.info("--- Asking Question using RAG System ---")
        files_to_query = [dummy_file, "non_existent.txt"]
        response = rag.ask(email, files_to_query, "What is SOLID?")
        
        logger.info("Response:")
        for line in response:
            logger.info(f"- {line}")
            
        # 4. Delete File
        logger.info(f"--- Deleting {dummy_file} ---")
        delete_msg = rag.delete(email, dummy_file)
        logger.info(delete_msg)
        
        # 5. Verify Deletion
        logger.info("--- Listing Files After Deletion ---")
        files_after = rag.list_files(email)
        logger.info(f"User files: {files_after}")

    finally:
        # Cleanup
        user_dir = os.path.join("uploads", email)
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)
        if os.path.exists(dummy_file):
            os.remove(dummy_file)