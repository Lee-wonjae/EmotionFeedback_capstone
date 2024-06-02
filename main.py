from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import byProfile, byScenario, postVideo
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 허용할 도메인 리스트
origins = [
    "http://localhost:8080",
    "http://43.203.209.38:8080",
    "http://localhost:3000",
    "http://localhost:8000"
]

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)

app.include_router(byProfile.router)
app.include_router(byScenario.router)
app.include_router(postVideo.router)