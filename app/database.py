from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:asdf25345@localhost/fastapi'
                          #'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
                           
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False ,autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
# get a connection with the database
# "db" in main
def get_db():
    db = SessionLocal()   # session object : responsible for talking with the databases
    try:
        yield db
    finally:
        db.close()

#----------------------------------------

while True:

    try :
        # Connect to an existing database
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='asdf25345', cursor_factory=RealDictCursor)

         # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("喵喵我成功了")    
        break  

    except Exception as error :
        print("喵喵我失敗了")
        print("Error : ", error)
        time.sleep(2)     #如失敗，每兩秒顯示一次error  
#----------------------------------------