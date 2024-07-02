from fastapi import  FastAPI, Depends, Request, Header, HTTPException
import httpx
import asyncio

app = FastAPI()

# 의존성 오버라이딩
def dependency():
    return {"key": "original"}

@app.get("/")
def main(dep=Depends(dependency)):
    return dep

def override_dependency():
    return {"key": "overridden"}

app.dependency_overrides[dependency] = override_dependency

# 클래스 기반 의존성
class DatabaseConnection:
    def __init__(self, db_url: str):
        self.db_url = db_url
class Repo:
    def __init__(self, conn: DatabaseConnection = Depends()):
        self.conn = conn

@app.get("/repo_items/")
def read_items(repo: Repo = Depends()):
    return {"db_url": repo.conn.db_url}

# 사용자 정의 종속성을 반환하는 복잡한 의존성
def get_query():
    return {"q": "fastapi"}

def get_db():
    return{"db": "test_db"}

def complex_dependency(query=Depends(get_query), db=Depends(get_db)):
    return {"query": query, "db": db}

@app.get("/complex")
def read_complex_data(data=Depends(complex_dependency)):
    return data

# 스코프, 생명주기
class ScopedConnection:
    def __init__(self, requests: Request):
        self.request = requests

@app.get("/scoped_items/")
async def read_scoped_items(conn: ScopedConnection = Depends(ScopedConnection)):
    return {"status": "new connection for each request"}

# 데이터베이스 연결을 시뮬레이션하는 클래스
class DBConnection:
    def __init__(self):
        self.conn = "Database Connection"

    async def __call__(self):
        # 실제 환경에서는 여기에서 데이터베이스 연결 로직을 실행
        return self.conn

# 의존성 인스턴스를 생성
db_connection = DBConnection()

# 의존성 함수
async def get_db_connection():
    return await db_connection()

# FastAPI 경로 작업
@app.get("/items/")
async def read_items(conn: str = Depends(get_db_connection, use_cashe=True)):
    # 첫 번째 호출에서 의존성을 계산하고, 같은 요청 동안의 후속 호출에서 캐시된 값을 사용.
    return {'database_connection': conn}

@app.get("/more-data/")
async def read_more_data(conn: str = Depends(get_db_connection, use_cache=True)):
    # 같은 요청에서 이전에 캐시된 데이터베이스 연결을 재사용합니다.
    return {"database_connection": conn}

# 의존성의 비동기 지원
async def get_remote_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
    
@app.get("/external")
async def external_data(data: dict = Depends(get_remote_data)):
    return data