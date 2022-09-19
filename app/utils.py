# we want to extract all of the hashing logic and store it in its own function 

from passlib.context import CryptContext

# telling passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# define the function we can call
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)