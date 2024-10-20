from sqlalchemy import Column, Integer, String
from .database import Base


class ArchitectureBlog(Base):
    __tablename__ = "architecture_blog"

    id = Column(Integer, primary_key=True, index=True)
    photo = Column(String, nullable=True)
    file = Column(String, nullable=True)
    description = Column(String, nullable=True)
