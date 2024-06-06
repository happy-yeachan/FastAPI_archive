from pydantic import BaseModel, validator

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.0

item = Item(name="Apple", descriptoin="Red fruit", price=5.5)

item_json = item.json()

item = Item.parse_raw(item_json)


class User(BaseModel):
    name: str
    age: int

    @validator('age')
    def check_age(cls, v):
        if v < 18:
            raise ValueError('Age must be at least 18')
        return v