from sqlalchemy.orm import Session
from .models import BlogPost
from .schemas import BlogPostCreate, BlogPostUpdate

def get_blog_post(db: Session, post_id: int):
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()

def get_blog_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(BlogPost).offset(skip).limit(limit).all()

def create_blog_post(db: Session, blog_post: BlogPostCreate):
    db_blog_post = BlogPost(**blog_post.dict())
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post


def delete_blog_post(db: Session, post_id: int):
    db.query(BlogPost).filter(BlogPost.id == post_id).delete()
    db.commit()
    return True


def update_blog_post(db: Session, post_id: int, blog_post: BlogPostUpdate):
    db.query(BlogPost).filter(BlogPost.id == post_id).update(blog_post.model_dump())
    db.commit()
    return get_blog_post(db, post_id=post_id)
