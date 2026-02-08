from typing import List
from sqlalchemy.orm import Session
from ..models.file import File
from .base_repository import BaseRepository

class FileRepository(BaseRepository[File]):
    def __init__(self, db: Session):
        super().__init__(db, File)

    def get_by_user_id(self, user_id: int) -> List[File]:
        return self.db.query(File).filter(File.user_id == user_id).all()

    def get_by_filenames(self, user_id: int, filenames: List[str]) -> List[File]:
        return self.db.query(File).filter(
            File.user_id == user_id,
            File.filename.in_(filenames)
        ).all()
