# .env 파일에서 DB 주소를 읽어서 PostgreSQL에 연결하는 파일

from sqlalchemy import create_engine #sqlalchemy:Python과 PostgreSQL을 연결해주는 도구
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv #dotenv : .env 파일을 읽어주는 도구
import os #os : Python 기본 내장 도구, 환경변수 읽을 때 사용

# .env 파일에서 환경변수 불러오기
# .env 파일에 저장해둔 DB 주소를 가져옴
load_dotenv() #dotenv : .env 파일을 읽어주는 도구
DATABASE_URL = os.getenv("DATABASE_URL")

# DB 연결 엔진 생성 (PostgreSQL에 실제로 연결하는 엔진)
engine = create_engine(DATABASE_URL)

# DB 세션 생성
# DB와 실제로 대화하는 창구

# autocommit=False : 실수로 저장되는 것을 방지/직접 저장 명령을 해야 저장 됨
# autoflush=False : 자동으로 DB에 반영하지 않음
# bind=engine : 위에서 만든 엔진에 연결
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테이블 정의할 때 사용할 Base 클래스 (models.py에서 모든 테이블이 Base를 상속받음)
Base = declarative_base()


# API에서 DB 연결할 때 사용하는 함수 (def : Python에서 함수를 정의할 때 항상 씀)
# def : 함수를 정의할 때 쓰는 키워드 (함수는 필요할 때마다 반복해서 실행)
# 위에 애들은 '변수' : 값을 저장하는 공간 (변수는 딱 한 번만 실행/결과 저장)
# def 있으면 함수 정의 / def 없으면 변수에 값 저장
def get_db():
    db = SessionLocal() # 함수 안에서 db변수 생성
    try:
        yield db # db를 API에 전달
        # return : 값을 돌려주고 함수 끝남
        # yield : 값을 돌려주고 함수가 끝나지 않고 대기
    finally:
        db.close() # 사용 끝나면 닫기
# yield : DB, 파일, 네트워크 연결처럼 열면 반드시 닫아야 할 때 씀
# return : 그냥 계산하거나 데이터 조회할 때 씀