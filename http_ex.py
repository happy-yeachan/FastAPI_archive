import logging
from fastapi import FastAPI, Form

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 간단한 데이터 저장소
items = {"1":{"name":"Pen"}, "2":{"name":"Pencil"}}

@app.get("/items")
async def read_items():
    logger.info("Fetching all items")
    return items

@app.post("/items/{items_id}")
async def create_item(item_id: str, name: str = Form(...)):
    items[item_id] = {"name": name}
    logger.info(f"Item created: {item_id} - {name}")
    return items[item_id]

@app.put("/items/{item_id}")
async def update_item(item_id: str, name: str = Form(...)):
    items[item_id] = {"name": name}
    logger.info(f"Item updated: {item_id} - {name}")
    return items[item_id]

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if item_id in items:
        del items[item_id]
        logger.info(f"Item deleted: {item_id}")
        return {"message": "Item deleted"}
    else:
        logger.info(f"Item not found: {item_id}")
        return {"message": "Item not found"}
    
@app.patch("/items/{item_id}")
async def patch_item(item_id: str, name: str = Form(...)):
    if item_id in items:
        items[item_id]["name"] = name
        logger.info(f"Item patched: {item_id} - {name}")
        return items[item_id]
    else:
        logger.info(f"Item not found: {item_id}")
        return {"message": "Item not found"}