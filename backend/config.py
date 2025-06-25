"""
환경 설정 관리
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """애플리케이션 설정"""
    
    # Google API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # LangSmith (선택사항)
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "product-search-agent")
    
    # 서버 설정
    HOST = os.getenv("BACKEND_HOST", os.getenv("HOST", "127.0.0.1"))
    PORT = int(os.getenv("BACKEND_PORT", os.getenv("PORT", "8000")))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))
    
    @classmethod
    def validate(cls):
        """필수 환경 변수 확인"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
        
        return True

# 설정 인스턴스
config = Config()

# 환경 변수 설정 가이드 출력
def print_env_guide():
    """환경 변수 설정 가이드 출력"""
    print("=" * 50)
    print("환경 변수 설정 가이드")
    print("=" * 50)
    print("다음 환경 변수들을 설정하세요:")
    print("export GOOGLE_API_KEY='your_google_api_key_here'")
    print("export LANGCHAIN_API_KEY='your_langchain_api_key_here'")
    print("export LANGCHAIN_TRACING_V2='true'")
    print("export LANGCHAIN_PROJECT='product-search-agent'")
    print("=" * 50)