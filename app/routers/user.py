from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter # router
from .. import models, schemas, utils
from ..database import get_db  # don't need to import engine, just leave it main.py file

# router object to be able to split off all of the rout or operation to different files 
router = APIRouter(
    prefix="/users",      # prefix(前綴) : so we don't need to write "/users" everywhere
    tags=['Users']       # so that we can have Users at http://127.0.0.1:8000/docs
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # so that the password will be protected

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# retrieve the information from specific user
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db :Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detailed=f"User with id: {id} does not exist")

    return user 