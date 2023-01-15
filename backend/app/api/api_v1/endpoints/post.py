from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.crud import crud_post
from app.db.init_db import get_db
from app.schemas.post_schema import PostBase, PostDisplay
import string
import random
import shutil

post_router = APIRouter(
    prefix="/post",
    tags=["post"]
)

@post_router.get("/")
async def fetch_post(db: Session = Depends(get_db)):
    return await crud_post.CRUDPost.get(db=db)

@post_router.post("/")
async def create_post(post_in: PostBase, db: Session = Depends(get_db)):
    return await crud_post.CRUDPost.create(request=post_in, db=db)

@post_router.post("/image")
async def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

@post_router.delete("/{id}")
async def fetch_post(id: int, db: Session = Depends(get_db)):
    return await crud_post.CRUDPost.delete(id=id, db=db)