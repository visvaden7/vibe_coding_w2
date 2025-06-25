"""
TASK-003: LangGraph Agent 테스트
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from backend.agent import AgentService


class TestAgentService:
    """Agent 서비스 테스트"""
    
    def setup_method(self):
        """테스트 설정"""
        # 환경 변수 설정
        os.environ["GOOGLE_API_KEY"] = "test_key"
        self.agent_service = AgentService()
    
    def test_agent_initialization(self):
        """Agent 초기화 테스트"""
        assert self.agent_service is not None
        assert hasattr(self.agent_service, 'agent')
        assert hasattr(self.agent_service, 'search_product')
    
    def test_search_product_with_valid_query(self):
        """유효한 검색 쿼리로 상품 검색 테스트"""
        query = "노트북"
        result = self.agent_service.search_product(query)
        
        assert result is not None
        assert isinstance(result, dict)
        assert "query" in result
        assert "products" in result
        assert result["query"] == query
        assert isinstance(result["products"], list)
    
    def test_search_product_with_empty_query(self):
        """빈 검색 쿼리 테스트"""
        query = ""
        result = self.agent_service.search_product(query)
        
        assert result is not None
        assert isinstance(result, dict)
        assert "error" in result
    
    @patch('langchain_community.tools.DuckDuckGoSearchRun.invoke')
    def test_duckduckgo_tool_integration(self, mock_search):
        """DuckDuckGo 도구 통합 테스트"""
        # Mock 설정
        mock_search.return_value = "샘플 검색 결과"
        
        query = "스마트폰"
        result = self.agent_service.search_product(query)
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_agent_response_format(self):
        """Agent 응답 형식 테스트"""
        query = "태블릿"
        result = self.agent_service.search_product(query)
        
        # 응답 형식 검증
        assert isinstance(result, dict)
        if "products" in result:
            for product in result["products"]:
                assert isinstance(product, dict)
                assert "name" in product
                assert "description" in product
                assert "price" in product
    
    def test_single_turn_behavior(self):
        """단일 턴 동작 테스트 (메모리 없음)"""
        query1 = "노트북"
        query2 = "게임용 노트북"
        
        result1 = self.agent_service.search_product(query1)
        result2 = self.agent_service.search_product(query2)
        
        # 각 쿼리는 독립적으로 처리되어야 함
        assert result1["query"] == query1
        assert result2["query"] == query2
        
        # 이전 검색 결과에 영향받지 않아야 함
        assert result1 != result2


class TestAgentTools:
    """Agent 도구 테스트"""
    
    def test_duckduckgo_tool_availability(self):
        """DuckDuckGo 도구 사용 가능성 테스트"""
        from langchain_community.tools import DuckDuckGoSearchRun
        
        search_tool = DuckDuckGoSearchRun()
        assert search_tool is not None
        assert hasattr(search_tool, 'invoke')
    
    def test_gemini_model_configuration(self):
        """Gemini 모델 설정 테스트"""
        os.environ["GOOGLE_API_KEY"] = "test_key"
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0,
            google_api_key="test_key"
        )
        assert model is not None
        assert model.model == "gemini-2.0-flash-exp"


if __name__ == "__main__":
    pytest.main([__file__])