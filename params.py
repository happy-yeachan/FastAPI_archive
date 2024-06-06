from fastapi import FastAPI, Request, Form, Header, Cookie

app = FastAPI()

# /items/?q=foo&q=bar
@app.get("/items")
async def read_items(q: list[str] = None):
    query_items = {"q":q}
    return {"message": query_items}

@app.post("/items/")
async def create_item(request: Request):
    data = await request.json()
    # 'data'는 파이썬 딕셔너리
    return data


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return{"username": username, "password":password}

@app.get("/items1")
async def read_items(user_agent: str = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/items/")
async def read_items(ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}