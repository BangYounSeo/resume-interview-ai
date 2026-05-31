# DB 설계에서 정의한 5개 테이블을 Python 코드로 작성하는 파일

# SQLAlchemy에서 테이블 컬럼 타입들 가져오기
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

# 테이블 간 관계 설정할 때 사용
from sqlalchemy.orm import relationship

# 날짜/시간 기본값 설정할 때 사용
from datetime import datetime

# database.py에서 만든 Base 클래스 가져오기
# 모든 테이블은 Base를 상속받아야 PostgreSQL에 테이블로 인식됨
from database import Base


# 회원 테이블

# class : 변수와 함수를 묶어서 하나의 틀을 만드는 것 (변수:저장소/함수:레시피/클래스:붕어빵 틀)
class User(Base):
    # __(언더스코어) : 특별한 의미를 가진 예약어라는 뜻
    # 언더스코어가 없으면 SQLAlchemy가 테이블 이름으로 인식하지 못함
    __tablename__ = "users" # PostgreSQL에 생성될 실제 테이블 이름
    
    id = Column(Integer, primary_key=True, index=True) # DB가 자동 부여하는 고유번호
    username = Column(String, unique=True, nullable=False) # nullable : 비어있어도 되냐? false = 안 됨
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now) # 가입날짜와 시간 자동으로 채워줌
    
    # 이 유저의 이력서 목록들 
    # relationship : 컬럼이 아님/ DB에 저장 안 됨, python에서만 존재 함
    resumes = relationship("Resume", back_populates="user") # User와 Resume가 1:N 관계임을 설정 (유저 한 명이 이력서 여러 개 가능)
    # ForeignKey : DB에서 실제로 연결하는 것 (필수)
    # relationship : Python 코드에서 편하게 접근하기 위한 것 (편의용)
    

# 이력서 테이블
class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # 어떤 유저의 이력서인지
    file_name = Column(String, nullable=False) # 업로드한 파일명
    extracted_text = Column(Text, nullable=False) # PDF에서 추출한 텍스트
    uploaded_at = Column(DateTime, default=datetime.now)
    
    # 이 이력서의 주인 유저
    user = relationship("User", back_populates="resumes") # Resume가 User에 속함을 설정
    questions = relationship("InterviewQuestion", back_populates="resume")  # Resume와 InterviewQuestion이 1:N 관계임을 설정
    

# 면접 질문 테이블 (AI가 생성한 질문 저장)
class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False) # 어떤 이력서 기반인지
    category = Column(String, nullable=False) # 질문 카테고리 (기술/경험/인성)
    question = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    resume = relationship("Resume", back_populates="questions") # InterviewQuestion이 Resume에 속함을 설정
    answers = relationship("UserAnswer", back_populates="question") # InterviewQuestion과 UserAnswer가 1:N 관계임을 설정


# 유저 답변 테이블
class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("interview_questions.id"), nullable=False)  # 어떤 질문에 대한 답변인지
    answer_text = Column(Text, nullable=False) # 유저가 작성한 답변
    ai_feedback = Column(Text, nullable=True) # AI가 생성한 피드백 (처음엔 비어있어도 됨)
    answered_at = Column(DateTime, default=datetime.now)

    # UserAnswer가 InterviewQuestion에 속함을 설정
    question = relationship("InterviewQuestion", back_populates="answers")
    
    
# RAG용 면접 데이터 테이블 (개발자가 미리 수집해서 넣어두는 원본 데이터)
class InterviewData(Base):
    __tablename__ = "interview_data"

    id = Column(Integer, primary_key=True, index=True)
    job_category = Column(String, nullable=False) # 직무 (백엔드/프론트엔드/PM 등)
    question = Column(Text, nullable=False)  # 면접 질문 원본
    embedding = Column(Text, nullable=True) # 벡터값 (RAG 검색할 때 사용)
    # 임베딩 : 텍스트를 숫자 배열로 변환한 것
    source = Column(String, nullable=True) # 출처