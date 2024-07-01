from fastapi import FastAPI, Depends, HTTPException, Path

app = FastAPI()

# 의존성 함수
def get_current_user(token: str = Path(...)):
    if token != "supersecrettoken":
        raise HTTPException(status_code=400, detail="Invalid Token")
    return {"username": "admin"}

# API 엔드포인트
@app.get("/users/me/{token}")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user