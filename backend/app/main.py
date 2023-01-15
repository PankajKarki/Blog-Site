from fastapi import FastAPI
from app.db.init_db import Base, engine
from app.models import post_model
from app.api.api_v1.endpoints import post
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

post_model.Base.metadata.create_all(engine)

app.include_router(post.post_router)

app.mount("/images", StaticFiles(directory="images"), name="images")

origins =[
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)