from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)
# models.Base.metadata.create_all(bind=engine)#alembic now does this for us

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
        


# my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1},
#             {"title":"favourite foods", "content":"I like pizza", "id":2}]

# order of a path operation matters hence if 2 function have the same routing, 
# FastAPI starts checking from the top to the bottom

# @app.get("/posts/latest")
# def get_latest_posts():
#     post = my_posts[len(my_posts) - 1]
#     # return {"detail": post}
#     return post

# @app.get("/sqlalchemy")
# def test_posts(db:Session= Depends(get_db)):
#     posts = db.query(models.Post).all()
#     print(posts)
#     return {"data":"successful"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")#path operation more like routing
def root():
    return {"message": "Hello World"}


