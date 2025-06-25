import os
from pathlib import Path

def test_project_structure():
    """프로젝트 폴더 구조가 올바르게 생성되었는지 테스트"""
    # backend 폴더 존재 확인
    assert os.path.exists("backend"), "backend 폴더가 존재하지 않습니다"
    
    # frontend 폴더 존재 확인
    assert os.path.exists("frontend"), "frontend 폴더가 존재하지 않습니다"
    
    # requirements.txt 존재 확인
    assert os.path.exists("requirements.txt"), "requirements.txt 파일이 존재하지 않습니다"
    
    # .env 파일 존재 확인
    assert os.path.exists(".env"), ".env 파일이 존재하지 않습니다"

def test_backend_structure():
    """백엔드 폴더 구조 테스트"""
    assert os.path.exists("backend/__init__.py"), "backend/__init__.py 파일이 존재하지 않습니다"
    assert os.path.exists("backend/main.py"), "backend/main.py 파일이 존재하지 않습니다"

def test_frontend_structure():
    """프론트엔드 폴더 구조 테스트"""
    assert os.path.exists("frontend/app.py"), "frontend/app.py 파일이 존재하지 않습니다"

def test_requirements_txt_content():
    """requirements.txt 파일에 필요한 패키지들이 포함되어 있는지 테스트"""
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            content = f.read()
            
        # 필수 패키지들이 포함되어 있는지 확인
        required_packages = [
            "fastapi",
            "uvicorn",
            "streamlit",
            "langgraph",
            "langchain",
            "langchain-google-genai",
            "langchain-community",
            "python-dotenv",
            "pytest"
        ]
        
        for package in required_packages:
            assert package in content, f"{package} 패키지가 requirements.txt에 포함되지 않았습니다"

def test_env_file_structure():
    """환경 변수 파일 구조 테스트"""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            
        # 필수 환경 변수들이 포함되어 있는지 확인
        required_env_vars = [
            "GOOGLE_API_KEY",
            "LANGCHAIN_API_KEY",
            "LANGCHAIN_TRACING_V2"
        ]
        
        for env_var in required_env_vars:
            assert env_var in content, f"{env_var} 환경 변수가 .env 파일에 포함되지 않았습니다"

if __name__ == "__main__":
    # 개별 테스트 실행
    try:
        test_project_structure()
        print("✅ 프로젝트 구조 테스트 통과")
    except AssertionError as e:
        print(f"❌ 프로젝트 구조 테스트 실패: {e}")
    
    try:
        test_backend_structure()
        print("✅ 백엔드 구조 테스트 통과")
    except AssertionError as e:
        print(f"❌ 백엔드 구조 테스트 실패: {e}")
    
    try:
        test_frontend_structure()
        print("✅ 프론트엔드 구조 테스트 통과")
    except AssertionError as e:
        print(f"❌ 프론트엔드 구조 테스트 실패: {e}")
    
    try:
        test_requirements_txt_content()
        print("✅ requirements.txt 내용 테스트 통과")
    except AssertionError as e:
        print(f"❌ requirements.txt 내용 테스트 실패: {e}")
    
    try:
        test_env_file_structure()
        print("✅ .env 파일 구조 테스트 통과")
    except AssertionError as e:
        print(f"❌ .env 파일 구조 테스트 실패: {e}")