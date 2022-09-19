from ast import Str
from hashlib import algorithms_available
from os import access
from pydantic import BaseSettings

class Settings(BaseSettings):
    # provide the list of all of the environment variables that we need to set
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str 
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()