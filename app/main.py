from fastapi import FastAPI
from .database import engine
from .routers import post, user, auth, vote
from . import models
from . config import settings
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine) # responsable to create all our table based on the model we supply # if using alembic it-> can delete

# Something about building APIs, the @app works up to down, meaning the order of the functoin matters 
# and we need to be careful which funcion we put first, specially when the function @app takes a parameter e.g {id} 
app = FastAPI()

origins = []            # this section we define who can send us a API request, the ones that in our list, their request would go to the routes
                        # in lines 24-28 and those whos not in the list would be denied
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") # get request of http method and (/) says where in the url we wanna go. ("/") meaning homepage
def root():
    return {"message": "welcome to my API bitch"} # convert it to jason and sends it to the user












# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p 

# def  find_index_by_id(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
#     return None



