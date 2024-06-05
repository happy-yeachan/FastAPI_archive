from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "나는 예찬"}

@app.get("/test")
async def test():
    return {"message": "테스트 테스트"}