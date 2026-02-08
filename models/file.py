from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.config import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    path = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to User
    owner = relationship("models.user.User", back_populates="files")

    def __repr__(self):
        return f"<File(filename='{self.filename}')>"
