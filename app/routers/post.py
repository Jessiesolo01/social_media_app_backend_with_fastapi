from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2

# router = APIRouter()
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/posts", response_model=List[schemas.Post])#get operation of retrieving data
@router.get("/", response_model=List[schemas.PostOut])#get operation of retrieving data
# @router.get("/")
def get_posts(db:Session= Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # ////////SQL CODE
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==models.Post.id, isouter=
                 True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)

    # posts created by the current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()


    # return {"data":posts} 
    # return posts
    return posts



# @router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db:Session= Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):


    # print(post)
    # print(post.dict())
    # print(post.title)
    # print(post.published)
    # print(post.rating)


    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)

    # my_posts.append(post_dict)
#??????????????????????MORE VULNERABLE WAY TO INSERT INTO DATABASE
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")

#????????SAFEST WAY TO INSERT BY PARAMETERIZING TO AVOID SQL INJECTIONS and manipulate DATA
    # ///////SQL CODE
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()

    # ////////USING QUERIES
   
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    print(current_user.id)
    # print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())#unpack the dictionary using **
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
 
    # return {"data":new_post}
    return new_post


# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new post":f"title: {payLoad['title']} content: {payLoad['content']}"}

# to get individual post, where id in the path operation repreent the path parameter


# @router.get("/posts/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session= Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # print(id)
    # print(type(id))
    # post = find_post(int(id))

    # SQL QUERY
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()


    # print(test_post)
    # post = find_post(id)

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==models.Post.id, isouter=
                 True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        # response.status_code = 404

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message":f"The post with id {id} was not found"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found")
    # return {"post_detail":post}
    return post

# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # find the index in the array that has ther required id

    # my_posts.pop(index)

    #SQL QUERY
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id: {id} does not exist")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(index)
    #return{'message': 'post was successfully deleted'}#this would not show since fastapi 204 doesnt require anything to be sent since we deleted something 
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# SChema/pydantic models define the structure of a request and response. it detrmines what a user needs to prive to create a post e.g here we need title, conetent and published with may be 
# omitted since we have a defaulyt value for published. It is the one that uses BaseModel. It is found as a parameter in the function i.e post:Post and post.dict()
# SQLALCHEMY models is where we use Base in the models.py file are responsible for defining the columns of the table within postgres. It is used to query, create, delete and update entried withing the database e.g in db.query(models.Posts)
# technically we dont need pydantic or schema models but because this is an API whefe you have to specify what needs to be sent and received by the user i.e request and response

# @router.put("/posts/{id}", response_model=schemas.Post)
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # # whenever you want to make changes ton a database, do a conn.commit
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # index = find_index_post(id)
    # if updated_post == None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id: {id} does not exist")

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    # HARDCODED VERSION
    # post_query.update({'title':'hey this is my updated title', 'content':'this is my updated content'}, 
    #                   synchronize_session=False)

    # IDEAL VERSION
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # return {"data":post_query.first()}
    return post_query.first()