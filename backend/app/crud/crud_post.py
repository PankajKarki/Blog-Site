import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.post_schema import PostBase
from app.models.post_model import DbPost

class CRUDPost:
    @staticmethod
    async def get(db: Session):
        return db.query(DbPost).all()

    @staticmethod
    async def create(request: PostBase, db: Session):
        new_post = DbPost(
            image_url = request.image_url,
            title = request.title,
            content = request.content,
            creator = request.creator,
            timestamp = datetime.datetime.now()
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post

    @staticmethod
    async def delete(id: int, db: Session):
        post = db.query(DbPost).get(id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{id} not found'
            )
        db.delete(post)
        db.commit()
        return post