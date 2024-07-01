from tarfile import HeaderError
from unittest.mock import Base
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

def get_api_key(api_key: str= Header(...)):
    if api_key != "secret":
        raise HTTPException(status_code=400, detail="Invalid API Key")
    return api_key

def get_user(api_key: str = Depends(get_api_key)):
    return User(username="johndoe", email="yea@naver.com")

@app.get("/users/me", response_model=User)
def read_current_user(user:User = Depends(get_user)):
    return user