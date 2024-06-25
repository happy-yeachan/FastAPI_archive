import requests

def create_item(name, description, price):
    response = requests.post("http://127.0.0.1:8000/items/", json={"name": name, "description": description, "price": price})
    return response.json()

def get_item(item_id):
    response = requests.get(f"http://127.0.0.1:8000/items/{item_id}")
    return response.json()

print(create_item("샘플", "설명", 1000))
print(get_item(1))