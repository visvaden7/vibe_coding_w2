"""
FastAPI 백엔드 메인 애플리케이션
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from backend.agent import AgentService

# Pydantic 모델 정의
class HealthResponse(BaseModel):
    status: str
    message: str

class MessageResponse(BaseModel):
    message: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    query: str
    response: str = ""
    products: list = []
    error: str = ""

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Vibe Coding W2-1 API",
    description="FastAPI backend for product search chatbot",
    version="1.0.0"
)

# CORS 미들웨어 설정
origins = [
    "http://localhost:8501",  # Streamlit 기본 포트
    "http://127.0.0.1:8501",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent 서비스 초기화
try:
    agent_service = AgentService()
except Exception as e:
    print(f"Agent 초기화 실패: {e}")
    agent_service = None

# 루트 엔드포인트
@app.get("/", response_model=MessageResponse)
async def read_root() -> Dict[str, str]:
    """루트 엔드포인트"""
    return {"message": "Hello World"}

# 헬스체크 엔드포인트
@app.get("/health", response_model=HealthResponse)
async def health_check() -> Dict[str, str]:
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "message": "FastAPI backend is running"
    }

# 채팅 엔드포인트
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """채팅 API - Agent를 통한 상품 검색"""
    if not agent_service:
        raise HTTPException(
            status_code=500, 
            detail="Agent 서비스가 초기화되지 않았습니다."
        )
    
    try:
        # Agent를 통한 상품 검색
        result = agent_service.search_product(request.message)
        
        # 응답 형식 통일
        response = ChatResponse(
            query=result.get("query", request.message),
            response=result.get("response", ""),
            products=result.get("products", []),
            error=result.get("error", "")
        )
        
        return response.dict()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"검색 처리 중 오류가 발생했습니다: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)