from pydantic import BaseModel
from typing import Optional

class ItBlogBase(BaseModel):
    title: str
    content: str
    post_url: Optional[str] = None
    
class ItBlogCreate(ItBlogBase):
    title: str
    content: str

class ItBlogUpdate(ItBlogBase):
    id: int 

class ItBlogResponse(ItBlogBase):
    id: int 
    post_url: Optional[str] = None  # URL to the uploaded file

    class Config:
        orm_mode = True
