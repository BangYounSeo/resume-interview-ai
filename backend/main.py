# FastAPI 앱 생성
from fastapi import FastAPI

# database.py에서 engine과 Base 가져오기
from database import engine, Base

# models.py에 정의된 테이블들을 인식시키기 위해 import
import models

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 서버 시작할 때 models.py에 정의된 테이블들을 PostgreSQL에 자동 생성
Base.metadata.create_all(bind=engine)

# 서버 정상 작동 확인용 API
@app.get("/")
def root():
    return {"message": "서버 정상 작동 중"}


# import models
# models 전체를 가져와서 SQLAlchemy가 테이블 정의를 인식하게 함
# 직접 models.User 이렇게 쓸 일은 없음

# from database import engine, Base
# database.py에서 engine이랑 Base만 골라서 가져옴
# 바로 engine, Base로 사용