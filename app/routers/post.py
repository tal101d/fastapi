from sqlalchemy import func
from .. import models , schemas , oauth2
from ..database import engine,get_db
from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/posts",tags=["Posts"])                              # router is an APIrouter instance that help us to route between the main.py that gets the request
                                                                                # to this file when we may have the disire functenality. the prefix sets the prefix of all functions
                                                                                # so we won't be needing to write it again and again every function

# @router.get("/", response_model=List[schemas.PostOut]) it didn't work
@router.get("/", response_model=List[schemas.Post])

def get_posts(db : Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int= 0, search: Optional[str]= ""):
    

                                                                                # cursor.execute(""" SELECT * FROM posts """) this concept is using raw SQL to manage the Database
                                                                                # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post).all()

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)        forsome reason i didn't work
    return posts
    
#@router.get("/{id}", response_model=schemas.PostOut)                               # the id is always be a string, so if we expect a number we need to convert it to an int type
@router.get("/{id}", response_model=schemas.Post)                               # the id is always be a string, so if we expect a number we need to convert it to an int type
def get__post_id (id: int, response: Response, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
                                                                                # cursor.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id),)) # we convert the id from str to int and back to str because we need the validate this agrument as int when the user passes it in the query
                                                                                # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(                 ### Didn't work ###   
    #      models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail={"message" : f"post with {id} was not found"})

    return post
    

    
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    # models.Post(title=post.title, content=post.content, published=post.published) == models.Post(**post.dict())
    # we implement unpacking, the reason to do that is the question: "what if we had a model(table) with 50 entries?"

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # the equvalnet to RENURNING func in SQL and it revtrive the data to the new_post variable
    return new_post

                                                                # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",
                                                                # (post.title,post.content,post.published))
                                                                # new_post = cursor.fetchone()
                                                                # conn.commit()    # MUST DO in order to save thing into the actual database(postgres)

    




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
                                                                # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
                                                                # deleted_post = cursor.fetchone()
                                                                # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exists]") 
    
    if post.owner_id != current_user.id:                        # Only the user can delete its own post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to preform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # when we delete data we don't expect a data back to return
                                                                # so the convetion is to returnt the HTTP responses
    




@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
                                                                # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *""" ,
                                                                #                 (post.title,post.content, post.published,str(id)))
                                                                # updated_post = cursor.fetchone()
                                                                # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_up = post_query.first()
    
    if post_up == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exists]") 
    
    if post_up.owner_id != current_user.id:                     # # Only the user can Update its own post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to preform requested action")


    post_query.update(post.model_dump(), synchronize_session=False) # instead of using post.dict() its better using post.model_dump(), idk maybe it's more efficient
    db.commit()

    return post_query.first()
    