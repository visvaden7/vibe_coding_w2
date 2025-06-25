"""
Streamlit 프론트엔드 애플리케이션
"""

import streamlit as st
import requests
from contextlib import contextmanager
from typing import Dict, Any, Optional
import time

# 상수 정의
API_BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{API_BASE_URL}/chat"

def get_api_endpoint() -> str:
    """API 엔드포인트 반환"""
    return API_ENDPOINT

def initialize_session_state() -> None:
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def add_message_to_history(role: str, content: str) -> None:
    """메시지를 히스토리에 추가"""
    st.session_state.messages.append({
        "role": role,
        "content": content
    })

def display_chat_history() -> None:
    """채팅 히스토리 표시"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def call_backend_api(message: str) -> str:
    """백엔드 API 호출"""
    try:
        response = requests.post(
            API_ENDPOINT,
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "응답을 받지 못했습니다.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
        return "죄송합니다. 서버 연결에 문제가 있어 응답을 받을 수 없습니다. 잠시 후 다시 시도해주세요."
    
    except Exception as e:
        st.error(f"예상치 못한 오류가 발생했습니다: {str(e)}")
        return "죄송합니다. 예상치 못한 오류가 발생했습니다. 잠시 후 다시 시도해주세요."

def process_user_input(user_input: str) -> None:
    """사용자 입력 처리"""
    # 빈 입력이나 공백만 있는 입력 처리
    if not user_input or not user_input.strip():
        return
    
    # 사용자 메시지 추가 및 표시
    add_message_to_history("user", user_input)
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 어시스턴트 응답 생성 및 표시
    with st.chat_message("assistant"):
        with st.spinner("답변을 생성하고 있습니다..."):
            response = call_backend_api(user_input)
        
        # 스트리밍 효과로 응답 표시
        response_placeholder = st.empty()
        displayed_response = ""
        
        for char in response:
            displayed_response += char
            response_placeholder.markdown(displayed_response + "▌")
            time.sleep(0.01)  # 타이핑 효과
        
        response_placeholder.markdown(displayed_response)
    
    # 어시스턴트 응답을 히스토리에 추가
    add_message_to_history("assistant", response)

def setup_app_ui() -> None:
    """앱 UI 설정"""
    st.title("🤖 AI 상품 검색 챗봇")
    st.markdown("""
    안녕하세요! 저는 상품 검색을 도와드리는 AI 어시스턴트입니다.
    
    **사용법:**
    - 찾고 싶은 상품에 대해 자유롭게 질문해주세요
    - 예: "노트북 추천해줘", "가성비 좋은 스마트폰 알려줘"
    
    궁금한 것이 있으시면 언제든 물어보세요! 😊
    """)
    st.divider()

def display_error_message(error_msg: str) -> None:
    """에러 메시지 표시"""
    st.error(error_msg)

@contextmanager
def show_loading_spinner(message: str):
    """로딩 스피너 컨텍스트 매니저"""
    with st.spinner(message):
        yield

def render_chat_interface() -> None:
    """채팅 인터페이스 렌더링"""
    # 채팅 히스토리 표시
    display_chat_history()
    
    # 사용자 입력 처리
    if prompt := st.chat_input("상품에 대해 궁금한 것을 물어보세요..."):
        process_user_input(prompt)

def main() -> None:
    """메인 함수"""
    # 페이지 설정
    st.set_page_config(
        page_title="AI 상품 검색 챗봇",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # UI 설정
    setup_app_ui()
    
    # 채팅 인터페이스 렌더링
    render_chat_interface()

if __name__ == "__main__":
    main()