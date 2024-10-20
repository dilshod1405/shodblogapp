from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, Request
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .crud import create_blog, get_blog, update_blog, delete_blog
from .schemas import ItBlogCreate, ItBlogResponse, ItBlogUpdate
import os
from fastapi.middleware.cors import CORSMiddleware
from .models import ItBlog
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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/upload/")
async def upload_blog(
    request: Request,
    title: str = File(...), 
    content: str = File(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Save the file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Generate the full URL for the uploaded file dynamically
    file = f"{request.url.scheme}://{request.url.netloc}/uploads/{file.filename}"

    # Create the blog entry
    blog_data = ItBlogCreate(
        title=title,
        content=content,
        post_url=file
    )

    blog_response = create_blog(db=db, blog=blog_data)  # Only pass post_url once
    
    return {
        "id": blog_response.id,
        "title": blog_response.title,
        "content": blog_response.content,
        "post_url": blog_response.post_url  # Return the dynamically generated URL
    }


@app.get("/itblogs/")
async def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(ItBlog).all()  # Fetch all blogs
    return blogs  # This will include the post_url

@app.get("/itblogs/{blog_id}", response_model=ItBlogResponse)
async def read_blog(blog_id: str, db: Session = Depends(get_db)):
    blog = get_blog(db, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.put("/itblogs/{blog_id}", response_model=ItBlogResponse)
async def update_existing_blog(blog_id: str, blog: ItBlogUpdate, db: Session = Depends(get_db)):
    updated_blog = update_blog(db, blog_id, blog)
    if updated_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog

@app.delete("/itblogs/{blog_id}")
async def delete_existing_blog(blog_id: str, db: Session = Depends(get_db)):
    if not delete_blog(db, blog_id):
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"detail": "Blog deleted"}
