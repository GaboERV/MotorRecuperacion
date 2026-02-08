import os
import shutil
from database.config import get_db, Base, engine
from rag_system import RAGSystem
from services.file_service import FileService

if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Setup
    email = "gaboe@example.com"
    dummy_file = "check_file.txt"
    
    # Create a local dummy file
    with open(dummy_file, "w") as f:
        f.write("Content for checking file management.")

    # Initialize System with DB Session
    db = next(get_db())
    rag = RAGSystem(db)

    try:
        # 1. Upload
        print(f"--- Uploading {dummy_file} ---")
        with open(dummy_file, "rb") as f:
            data = f.read()
        rag.upload(email, dummy_file, data)
        
        # 2. List Files
        print("--- Listing Files ---")
        files = rag.list_files(email)
        print(f"Files: {files}")
        
        if dummy_file in files:
            print("SUCCESS: File listed correctly.")
        else:
            print("FAILURE: File not found in list.")

        # 3. Delete File
        print(f"--- Deleting {dummy_file} ---")
        result = rag.delete(email, dummy_file)
        print(result)
        
        # 4. Verify Deletion
        print("--- Listing Files After Deletion ---")
        files_after = rag.list_files(email)
        print(f"Files: {files_after}")

        if dummy_file not in files_after:
             print("SUCCESS: File deleted correctly.")
        else:
             print("FAILURE: File still present.")

    finally:
        # Cleanup
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
        user_dir = os.path.join("uploads", email)
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)
