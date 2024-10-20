from pydantic import BaseModel
from typing import Optional

class BlogPostBase(BaseModel):
    title: str
    photo: Optional[str] = None
    date: str
    content: str 

class BlogPostCreate(BlogPostBase):
    title: str
    date: str
    content: str

class BlogPostResponse(BlogPostBase):
    id: int
    photo: Optional[str] = None

    class Config:
        orm_mode = True


class BlogPostUpdate(BlogPostBase):
    pass
