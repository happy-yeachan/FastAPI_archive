from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, insert, update, delete, func

# 데이터 베이스 설정
engine = create_engine('sqlite:///example.db')
metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('age', Integer))
metadata.create_all(engine)

app = FastAPI()

# 사용자 데이터를 위한 Pydantic 모델
class User(BaseModel):
    name: str
    age: int

# 사용자 응답을 위한 Pydantic 모델
class UserResponse(BaseModel):
    id: int
    name: str
    age: int

# 사용자 업데이트를 위한 Pydantic 모델
class UserUpdate(BaseModel):
    name: str = None
    age: int = None

# 평균 연령 응답을 위한 Pydantic 모델
class AverageAgeResponse(BaseModel):
    name: str
    average_age: int

@app.get("/users/", response_model=List[UserResponse])
def read_users():
    with engine.connect() as conn:
        result = conn.execute(select(users))
        user_list = result.fetchall()
        return [UserResponse(id=row[0], name=row[1], age=row[2]) for row in user_list]

@app.post("/users/", response_model=UserResponse)
def create_user(user: User):
    with engine.connect() as conn:
        result = conn.execute(insert(users).values(name=user.name, age= user.age))
        conn.commit()
        new_user_id = result.lastrowid
        return UserResponse(id=new_user_id, name=user.name, age=user.age)

@app.put("users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user:UserUpdate):
    with engine.connect() as conn:
        update_stmt = update(users).where(users.c.id == user_id)
        if user.name:
            update_stmt = update_stmt.values(name=user.name)
        if user.age:
            update_stmt = update_stmt.values(age=user.age)
        conn.execute(update_stmt)
        conn.commit()
    return read_users(user_id)

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(select(users).where(users.c.id == user_id))
        user = result.fetchall()
        if user:
            return UserResponse(id=user[0], name=user[1], age=user[2])
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with engine.connect() as conn:
        conn.execute(delete(users).where(users.c.id == user_id))
        conn.commit()
    return {"message": "User deleted"}

