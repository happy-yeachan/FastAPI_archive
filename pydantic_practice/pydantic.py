from pydantic import BaseModel, validator
from typing import List

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.0

item = Item(name="Apple", descriptoin="Red fruit", price=5.5)
item_json = item.json()
print(item_json)
item = Item.parse_raw(item_json)


class User(BaseModel):
    name: str
    age: int

    @validator('age')
    def check_age(cls, v):
        if v < 18:
            raise ValueError('Age must be at least 18')
        return v
    
class Order(BaseModel):
    id: int
    items: List[Item]

order = Order(id=123, items=[{"name": "Apple", "price":5.5}, {"name": "Banana", "price": 3.0}])

class ORMModel:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class UserModel(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

orm_user = ORMModel(name="Alice", age=30)
user = UserModel.form_orm(orm_user)