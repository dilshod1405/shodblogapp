from sqlalchemy.orm import Session
from .models import ItBlog
from .schemas import ItBlogCreate, ItBlogUpdate
from typing import List

def create_blog(db: Session, blog: ItBlogCreate) -> ItBlog:
    db_blog = ItBlog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: str) -> ItBlog:
    return db.query(ItBlog).filter(ItBlog.id == blog_id).first()

def get_blogs(db: Session) -> List[ItBlog]:
    return db.query(ItBlog).all()

def update_blog(db: Session, blog_id: str, blog: ItBlogUpdate) -> ItBlog:
    db_blog = db.query(ItBlog).filter(ItBlog.id == blog_id).first()
    if db_blog:
        for key, value in blog.dict(exclude_unset=True).items():
            setattr(db_blog, key, value)
        db.commit()
        db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: str) -> bool:
    db_blog = db.query(ItBlog).filter(ItBlog.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return True
    return False
