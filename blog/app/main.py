from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .crud import create_blog_post, get_blog_posts, get_blog_post, delete_blog_post, update_blog_post
from .schemas import BlogPostCreate, BlogPostUpdate, BlogPostResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from mangum import Mangum


app = FastAPI()

handler = Mangum(app)
    
Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Post new blog
@app.post("/upload/")
async def upload_blog(
    request: Request,
    title: str = File(...), 
    date: str = File(...),
    content: str = File(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    file = f"{request.url.scheme}://{request.url.netloc}/uploads/{file.filename}"
    
    blog_data = BlogPostCreate(
        title=title,
        date=date,
        content=content,
        photo=file
    )
    
    blog_response = create_blog_post(db=db, blog_post=blog_data)
    
    return {
        "id": blog_response.id,
        "title": blog_response.title,
        "date": blog_response.date,
        "content": blog_response.content,
        "photo": blog_response.photo
    }

# Get all posts
@app.get("/blogs", response_model=list[BlogPostResponse])
async def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_blog_posts(db, skip=skip, limit=limit)


# Get single post
@app.get("/blogs/{post_id}", response_model=BlogPostResponse)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_blog_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


# Delete post
@app.delete("/blogs/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    return delete_blog_post(db, post_id=post_id)


# Update post
@app.put("/blogs/{post_id}", response_model=BlogPostResponse)
async def update_post(post_id: int, post: BlogPostUpdate, db: Session = Depends(get_db)):
    return update_blog_post(db, post_id=post_id, blog_post=post)