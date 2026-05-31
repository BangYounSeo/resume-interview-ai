from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "서버 정상 작동 중"}