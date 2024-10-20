from sqlalchemy import Column, String, Text, Integer
from .database import Base

class ItBlog(Base):
    __tablename__ = "itblogs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    content = Column(Text)
    post_url = Column(String)

