import os
import logging
from typing import List
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.file import File
from ..repositories.user_repository import UserRepository
from ..repositories.file_repository import FileRepository
from ..config import UPLOAD_DIR

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.file_repo = FileRepository(db)
        
        # Ensure upload directory exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

    def upload_file(self, user_email: str, filename: str, file_data: bytes) -> File:
        """
        Handles file upload from direct content (bytes):
        1. Gets or creates user.
        2. Saves content to `uploads/{user_email}/{filename}`.
        3. Creates/Updates File record in DB.
        """
        import shutil

        # 1. Get or Create User
        user = self.user_repo.get_by_email(user_email)
        if not user:
            user = User(email=user_email)
            user = self.user_repo.create(user)

        # 2. Prepare destination
        user_dir = os.path.join(UPLOAD_DIR, user_email)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        dest_path = os.path.join(user_dir, filename)

        # 3. Write file to destination
        with open(dest_path, "wb") as f:
            f.write(file_data)

        # 4. Create/Update File record
        existing_file = next((f for f in user.files if f.filename == filename), None)
        if existing_file:
            existing_file.path = dest_path
            return self.file_repo.update(existing_file)
        
        file_record = File(
            filename=filename,
            path=dest_path,
            user_id=user.id
        )
        return self.file_repo.create(file_record)

    def get_validated_file_paths(self, user_email: str, filenames: List[str]) -> List[str]:
        """
        Validates user and files, returning a list of valid local file paths.
        Raises specific exceptions or returns empty if validation fails.
        """
        # 1. Validate User
        user = self.user_repo.get_by_email(user_email)
        if not user:
            logger.warning(f"User not found: {user_email}")
            return []

        # 2. Get File records for this user matching requested filenames
        files = self.file_repo.get_by_filenames(user.id, filenames)
        
        valid_paths = []
        found_filenames = {f.filename for f in files}

        for filename in filenames:
            if filename not in found_filenames:
                logger.warning(f"File not found or not owned by user: {filename}")
                continue
            
            # Find the corresponding file record
            file_record = next(f for f in files if f.filename == filename)
            
            # 3. Verify file exists on disk
            if os.path.exists(file_record.path):
                valid_paths.append(file_record.path)
            else:
                logger.error(f"Physical file missing for: {filename} at {file_record.path}")

        return valid_paths

    def list_files(self, user_email: str) -> List[str]:
        """
        Returns a list of filenames uploaded by the user.
        """
        user = self.user_repo.get_by_email(user_email)
        if not user:
            return []
        return [f.filename for f in user.files]

    def delete_file(self, user_email: str, filename: str) -> bool:
        """
        Deletes a file from the database and disk.
        Returns True if deleted, False otherwise.
        """
        user = self.user_repo.get_by_email(user_email)
        if not user:
            return False

        files = self.file_repo.get_by_filenames(user.id, [filename])
        if not files:
            return False

        file_record = files[0]
        
        # 1. Delete from Disk
        if os.path.exists(file_record.path):
            try:
                os.remove(file_record.path)
            except OSError as e:
                logger.error(f"Error deleting file {file_record.path}: {e}")
                # Continue to delete DB record even if disk delete fails (or maybe it creates an inconsistency? 
                # Better to delete DB record so user doesn't see it anymore)

        # 2. Delete from DB
        self.file_repo.delete(file_record.id)
        return True
