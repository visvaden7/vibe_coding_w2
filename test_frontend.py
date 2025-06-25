import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import requests
import sys
import os

# Add frontend directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

class TestStreamlitFrontend:
    """Streamlit 프론트엔드 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행되는 설정"""
        # 세션 상태 초기화
        if hasattr(st, 'session_state'):
            st.session_state.clear()
    
    def test_session_state_initialization(self):
        """세션 상태 초기화 테스트"""
        from frontend.app import initialize_session_state
        
        # 세션 상태가 비어있을 때
        st.session_state.clear()
        initialize_session_state()
        
        # messages 키가 존재하고 빈 리스트인지 확인
        assert "messages" in st.session_state
        assert st.session_state.messages == []
        assert isinstance(st.session_state.messages, list)
    
    def test_display_chat_history(self):
        """채팅 히스토리 표시 테스트"""
        from frontend.app import display_chat_history
        
        # 테스트 메시지 데이터
        test_messages = [
            {"role": "user", "content": "안녕하세요"},
            {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}
        ]
        
        st.session_state.messages = test_messages
        
        # 채팅 히스토리 표시 함수 실행
        with patch('streamlit.chat_message') as mock_chat_message:
            display_chat_history()
            
            # chat_message가 메시지 개수만큼 호출되었는지 확인
            assert mock_chat_message.call_count == len(test_messages)
    
    def test_add_message_to_history(self):
        """메시지 히스토리 추가 테스트"""
        from frontend.app import add_message_to_history
        
        # 초기 상태
        st.session_state.messages = []
        
        # 사용자 메시지 추가
        add_message_to_history("user", "테스트 메시지")
        
        assert len(st.session_state.messages) == 1
        assert st.session_state.messages[0]["role"] == "user"
        assert st.session_state.messages[0]["content"] == "테스트 메시지"
        
        # 어시스턴트 메시지 추가
        add_message_to_history("assistant", "테스트 응답")
        
        assert len(st.session_state.messages) == 2
        assert st.session_state.messages[1]["role"] == "assistant"
        assert st.session_state.messages[1]["content"] == "테스트 응답"
    
    @patch('requests.post')
    def test_call_backend_api_success(self, mock_post):
        """백엔드 API 호출 성공 테스트"""
        from frontend.app import call_backend_api
        
        # Mock 응답 설정
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "테스트 응답"}
        mock_post.return_value = mock_response
        
        # API 호출
        result = call_backend_api("테스트 메시지")
        
        # 결과 확인
        assert result == "테스트 응답"
        mock_post.assert_called_once()
        
        # 호출 인자 확인
        call_args = mock_post.call_args
        assert call_args[1]['json']['message'] == "테스트 메시지"
    
    @patch('requests.post')
    def test_call_backend_api_error(self, mock_post):
        """백엔드 API 호출 에러 테스트"""
        from frontend.app import call_backend_api
        
        # Mock 에러 응답 설정
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        
        # API 호출
        result = call_backend_api("테스트 메시지")
        
        # 에러 메시지 반환 확인
        assert "죄송합니다" in result
        assert "서버 연결에 문제가 있어" in result
    
    def test_process_user_input(self):
        """사용자 입력 처리 테스트"""
        from frontend.app import process_user_input
        
        # 초기 상태
        st.session_state.messages = []
        
        # 사용자 입력 처리
        with patch('frontend.app.call_backend_api') as mock_api:
            mock_api.return_value = "테스트 응답"
            
            process_user_input("테스트 질문")
            
            # 메시지가 올바르게 추가되었는지 확인
            assert len(st.session_state.messages) == 2
            assert st.session_state.messages[0]["role"] == "user"
            assert st.session_state.messages[0]["content"] == "테스트 질문"
            assert st.session_state.messages[1]["role"] == "assistant"
            assert st.session_state.messages[1]["content"] == "테스트 응답"
            
            # API가 호출되었는지 확인
            mock_api.assert_called_once_with("테스트 질문")

if __name__ == "__main__":
    pytest.main([__file__])