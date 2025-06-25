"""
TASK-003: FastAPI 백엔드 테스트
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app


class TestBackendAPI:
    """백엔드 API 테스트"""
    
    def setup_method(self):
        """테스트 설정"""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
    
    def test_health_check(self):
        """헬스체크 엔드포인트 테스트"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
    
    @patch('backend.main.agent_service')
    def test_chat_endpoint_success(self, mock_agent_service):
        """채팅 엔드포인트 성공 테스트"""
        # Mock 설정
        mock_agent_service.search_product.return_value = {
            "query": "노트북",
            "response": "노트북 검색 결과입니다.",
            "products": [
                {
                    "name": "노트북 상품 1",
                    "description": "고성능 노트북",
                    "price": "1,000,000원",
                    "rating": "4.5/5",
                    "availability": "재고 있음"
                }
            ]
        }
        
        response = self.client.post("/chat", json={"message": "노트북"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["query"] == "노트북"
        assert "response" in data
        assert "products" in data
        assert len(data["products"]) > 0
    
    @patch('backend.main.agent_service')
    def test_chat_endpoint_error(self, mock_agent_service):
        """채팅 엔드포인트 에러 테스트"""
        # Mock 설정 - 에러 응답
        mock_agent_service.search_product.return_value = {
            "query": "테스트",
            "error": "검색 중 오류가 발생했습니다."
        }
        
        response = self.client.post("/chat", json={"message": "테스트"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["query"] == "테스트"
        assert data["error"] != ""
    
    def test_chat_endpoint_empty_message(self):
        """빈 메시지로 채팅 엔드포인트 테스트"""
        response = self.client.post("/chat", json={"message": ""})
        assert response.status_code == 200
        
        data = response.json()
        assert "error" in data
    
    def test_chat_endpoint_invalid_payload(self):
        """잘못된 페이로드로 채팅 엔드포인트 테스트"""
        response = self.client.post("/chat", json={})
        assert response.status_code == 422  # Validation error
    
    @patch('backend.main.agent_service', None)
    def test_chat_endpoint_agent_not_initialized(self):
        """Agent 서비스가 초기화되지 않은 경우 테스트"""
        response = self.client.post("/chat", json={"message": "테스트"})
        assert response.status_code == 500


class TestAPIModels:
    """API 모델 테스트"""
    
    def test_chat_request_model(self):
        """ChatRequest 모델 테스트"""
        from backend.main import ChatRequest
        
        request = ChatRequest(message="테스트 메시지")
        assert request.message == "테스트 메시지"
    
    def test_chat_response_model(self):
        """ChatResponse 모델 테스트"""
        from backend.main import ChatResponse
        
        response = ChatResponse(
            query="테스트",
            response="응답",
            products=[],
            error=""
        )
        assert response.query == "테스트"
        assert response.response == "응답"
        assert response.products == []
        assert response.error == ""


if __name__ == "__main__":
    pytest.main([__file__])