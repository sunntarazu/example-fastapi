from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2 # don't need to import "utils" cause we don't need security 
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",      # prefix(前綴) : so we don't need to write "/posts" everywhere
    tags=['Posts']       # so that we can have Posts at http://127.0.0.1:8000/docs
)

@router.get("/", response_model=List[schemas.PostOut])
#@router.get("/")
def get_posts(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10, skip = 0, search: Optional[str] = ""):
    # 限制顯示數量 {URL}posts?limit=3&skip=2&search=喵%20喵 : 搜尋關鍵字"喵 喵"，跳過前兩則，顯示三則，不限制則是照預設限制十則
    #                                                             (%20代表空格)

    # Execute a command: this creates a new table
    #cursor.execute("""SELECT * FROM posts""")
    #tt = cursor.fetchall()

    #print(limit)

    # to make user only able to see the post that is create by themselves, not public
    #tt = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 
    tt = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # isouter : outer join
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                isouter=True).group_by(models.Post.id).filter(
                    models.Post.title.contains(search)).limit(limit).offset(skip).all()
 
    return posts

# 兩個都是get("/") : 程式先讀到第一個，然後就回傳了，第二個並不會讀進去

#@app.post("/createposts")
#def create_posts(payload: dict = Body(...)):   # payload can be any name you want        # postman - Body - raw : type something
#    print(payload)
#    return {"new _post": f"title {payload['title']} content: {payload['content']}"}      
# And That's how we extract the data from the body of payload

# title str, content str, (category...)

                                                               #(當想要限定response給使用者的格式時)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    #print(create_post.rating)
    #print(create_post)
    #print(create_post.dict())
    #return {"data": "create post"}
    #return {"data": create_post}

    #tttt = create_post.dict()
    #tttt['id'] = randrange(0, 1000000)   #在Post之後新增id
    #tttt['id2'] = randrange(0,77)    #新增id2  這兩行演示如何新增元素到dict
    #tttt['我愛的人'] = '喵喵'    #新增元素
    #my_posts.append(tttt)    #在my_posts這個array最後再新增一個元素tttt
    #return {"data": my_posts}

    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(new_post.title, new_post.content, new_post.published))             
    #ff = cursor.fetchone()
    #conn.commit()              # To actually save the data into the postgre

    #print(current_user.id)
    #print(current_user.email)
    #new_post_post = models.Post(title=post.title, content=post.content, published=post.published)              # pass in the property
    new_post = models.Post(owner_id=current_user.id, **post.dict())     #跟上面那行功用一樣但精簡很多
    db.add(new_post)   #add it to the database
    db.commit()    #commit it 
    db.refresh(new_post)    # retrieve the new_post that we just created and back into the variable new_post

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)  #path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # Response to manipulate the response
    
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))  # (str(id)) translate id from int to string
    #post = cursor.fetchone()

    #yy = db.query(models.Post).filter(models.Post.id == id).first()

    yy = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    #post = find_post(id)
    if not yy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found") #raise...可以取代下面兩行
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}

    # to make user only able to see the post that is create by themselves, not public
    #if yy.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail="Not authorized to perform requested action")
    
    return  yy

#需宣告id的type (例如 : 字串 整數)


#@router.get("/posts/recent/latest")
#def get_latest_post():
    #post = my_posts[len(my_posts)-1]
    #return post

# ng : /posts/latest 在 /posts/{id} 的下面
# 因為上面宣告/posts/{id} 過了 而且id須為int
# latest在上面錯誤就會被擋下來了
# 所以如果真的要宣告/posts/latest要在/posts/{id} 上面
# 或是直接像recent這個直接再往下宣告一個路徑


#deleting post 刪除指定資源
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = deleted_post.first()

    # to find the index in the array that has required ID
    #index = find_index_post(id)

    #if index == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    #my_posts.pop(index)

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



#put : passing data for all of the fields
@router.put("/{id}", response_model=schemas.Post)   # user send id that post he want to update
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title, post.content, post.published, str(id,)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    uu = db.query(models.Post).filter(models.Post.id == id)    
    updated_post = uu.first()

    # to find the index in the array that has required ID
    #index = find_index_post(id)

    # if the id does NOT exist
    #if index == None:   
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id:{id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    #if the id DOES exist
    #post_dict = post.dict()   #convert it to a regular python dictionary
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    #return {"data": post_dict}

    # 直接在python說要增加什麼
    #uu.update({'title' : 'hey 你知道喵喵很可愛嗎', 'content' : '喵喵戴眼鏡很適合喔'}, synchronize_session=False)
    # 在Body中說要增加什麼
    uu.update(post.dict(), synchronize_session=False)
    db.commit()

    return uu.first()