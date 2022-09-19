from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


#BaseModel ： fur to our schema
#shape of the request
#class Post(BaseModel):  # Post can be any name
    #title: str = True
    #content: str   # title content 形式為str
    #published: bool = True
    #rating: Optional[int] = None
    #title: Union[str, bytes] = None
    #content: Optional[str] = None 
    # = True/None : 預設成true 或 null  沒有打東西則會跑出預設 有打東西則會希望符合str bool的設定 否則錯誤

#-----------------------------------------------

class CreatePost(BaseModel):
    title: str 
    content: str 
    published: bool = True

class UpdatePost(BaseModel):
    title: str 
    content: str 
    published: bool = True

# At this point, we can have two different classes for each specific request 
#-----------------------------------------------

class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True

#by default, automatically inherit all the fields of PostBase
class PostCreate(PostBase):
    pass #which means its just going to accept PostBase

#-----------------------------------------------

class UserCreate(BaseModel):
    email: EmailStr   # to ensure that is a valid email
    password: str

# to be the shape of our model that we send back to user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True  # to convert it from SQLAlchemy to Pydantic Model

#-----------------------------------------------

class PP(BaseModel):
    title: str
    content:str

# specify all of the fields that we want to response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True
# Pydnatic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model


class PostOut(BaseModel):
    Post: Post  #inherit
    votes: int

    class Config:
        orm_mode = True

#-----------------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

#-----------------------------------------------

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)



