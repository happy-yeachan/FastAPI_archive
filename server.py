import uvicorn


if __name__ == "__main__":
    uvicorn.run("http_ex:app", host="localhost", port= 8000, reload=False)