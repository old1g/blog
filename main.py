from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import BlogPost, SessionLocal

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for request and response
class BlogPostCreate(BaseModel):
    title: str
    content: str


class BlogPostResponse(BlogPostCreate):
    id: int


# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(BlogPost).all()
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})


# Read a single post
@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


# Create post form
@app.get("/create_post", response_class=HTMLResponse)
async def create_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


# Create a new post
@app.post("/create_post")
async def create_post(title: str = Form(...),
                      content: str = Form(...),
                      db: Session = Depends(get_db)):
    db_post = BlogPost(title=title, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return RedirectResponse("/", status_code=303)


# Delete a post
@app.post("/delete_post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse("/", status_code=303)