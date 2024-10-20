from sqlalchemy.orm import Session
from .models import ArchitectureBlog
from .schemas import ArchitectureCreate, ArchitectureUpdate
from typing import List


def create_blog(db: Session, blog: ArchitectureCreate) -> ArchitectureBlog:
    db_blog = ArchitectureBlog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def read_blog(db: Session, blog_id: int) -> ArchitectureBlog:
    return db.query(ArchitectureBlog).filter(ArchitectureBlog.id == blog_id).first()


def get_blogs(db: Session, skip: int = 0, limit: int = 10) -> List[ArchitectureBlog]:
    return db.query(ArchitectureBlog).offset(skip).limit(limit).all()


def update_blog(db: Session, blog_id: int, blog: ArchitectureUpdate) -> ArchitectureBlog:
    db_blog = read_blog(db, blog_id)
    if not db_blog:
        return None
    db_blog.photo = blog.photo
    db_blog.file = blog.file
    db_blog.description = blog.description
    db.commit()
    db.refresh(db_blog)
    return db_blog


def delete_blog(db: Session, blog_id: int) -> bool:
    db_blog = read_blog(db, blog_id)
    if not db_blog:
        return False
    db.delete(db_blog)
    db.commit()
    return True