from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .crud import create_blog, get_blogs, update_blog, delete_blog, read_blog
from .schemas import ArchitectureCreate, ArchitectureResponse, ArchitectureUpdate
import os
from mangum import Mangum


Base.metadata.create_all(bind=engine)


app = FastAPI()

handler = Mangum(app)


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
async def upload_blog(request: Request, description: str = File(...), file: UploadFile = File(...), db: Session = Depends(get_db), photo: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    file_location = os.path.join(UPLOAD_DIR, photo.filename)
    with open(file_location, "wb") as f:
        f.write(await photo.read())

    blog_data = ArchitectureCreate(
        description=description,
        file=f"{request.url.scheme}://{request.url.netloc}/uploads/{file.filename}",
        photo=f"{request.url.scheme}://{request.url.netloc}/uploads/{file.filename}"
    )

    blog_response = create_blog(db=db, blog=blog_data)

    return {
        "id": blog_response.id,
        "description": blog_response.description,
        "file": blog_response.file,
        "photo": blog_response.photo
    }


@app.get("/blogs", response_model=list[ArchitectureResponse])
async def read_blogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_blogs(db, skip=skip, limit=limit)


@app.put("/blogs/{blog_id}", response_model=ArchitectureResponse)
async def update_blog_by_id(blog_id: int, blog: ArchitectureUpdate, db: Session = Depends(get_db)):
    updated_blog = update_blog(db, blog_id, blog)
    if updated_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog


@app.delete("/blogs/{blog_id}")
async def delete_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    if not delete_blog(db, blog_id):
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"detail": "Blog deleted"}


@app.get("/blogs/{blog_id}", response_model=ArchitectureResponse)
async def read_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog =read_blog(db, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
