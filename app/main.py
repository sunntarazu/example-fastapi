from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# tell sqlalchemy to run the create statement that generate all the tables when we start it up 
#models.Base.metadata.create_all(bind=engine) #sql


# create an instance of API
app = FastAPI()  # can give app any name

#----------------------------------------
# provide a list of all the domains that can talk to our API
origins = ["https://www.google.com","https://www.youtube.com"]
#origins = ["*"]       # means every single domain or origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#----------------------------------------

#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{
#    "title": "favorite foods", "content": "I like pizza", "id": 2},{
#    "title": "我愛", "content": "喵喵", "id": 4}]


#def find_post(id):
#    for p in my_posts:
#        if p['id'] == id:
#            return p

#def find_index_post(id):
#    for i, p in enumerate(my_posts):
#        if p['id'] == id:
#            return i 


# test the Dependency
#@app.get("/sqlalchemy")
#def test_posts(db : Session = Depends(get_db)):    #db : Session = Depends(get_db) : make it the dependency

    #posts = db.query(models.Post).all()  # to grab every single entry within the post table 
    #return {"data" : posts}

    #posts = db.query(models.Post)  # to grab every single entry within the post table 
    #print(posts)
    #return {"data" : "meow"}
    

# import router in post and user
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# path operations
@app.get("/")  # @app : decorator  # 「get」可以請求展示指定資源，可以在HTTP　request看更多請求方式(method) 的功能
def root():  # root : function
    print("message", ": 我愛喵喵")
    return {"message": "welcome to my api!!!!!!!"}
# return : data that send back to users
# start the web server : terminal type "uvicorn app.main:app --reload"  (filename.filename:instance name)                                 
