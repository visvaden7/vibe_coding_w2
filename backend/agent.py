"""
TASK-003: LangGraph Agent 구현
React Agent를 사용한 상품 검색 서비스
"""

import os
from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from backend.config import Config


class AgentService:
    """LangGraph React Agent 서비스"""
    
    def __init__(self):
        """Agent 초기화"""
        self._initialize_model()
        self._initialize_tools()
        self._create_agent()
    
    def _initialize_model(self):
        """Gemini 모델 초기화"""
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
        
        # LangSmith 트레이싱 설정
        if Config.LANGSMITH_TRACING and Config.LANGSMITH_API_KEY:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = Config.LANGSMITH_API_KEY
            os.environ["LANGCHAIN_PROJECT"] = Config.LANGCHAIN_PROJECT
        
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0,
            google_api_key=Config.GOOGLE_API_KEY
        )
    
    def _initialize_tools(self):
        """도구 초기화"""
        # DuckDuckGo 검색 도구
        self.search_tool = DuckDuckGoSearchRun()
        self.tools = [self.search_tool]
    
    def _create_agent(self):
        """React Agent 생성"""
        system_prompt = """
        당신은 상품 검색 전문 어시스턴트입니다.
        사용자가 요청하는 상품에 대해 웹 검색을 통해 정보를 찾아 제공해주세요.
        검색 결과를 바탕으로 상품 정보를 정리해서 응답해주세요.
        """
        
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=system_prompt
        )
    
    def search_product(self, query: str) -> Dict[str, Any]:
        """상품 검색 실행"""
        if not query or not query.strip():
            return {"error": "검색 쿼리가 비어있습니다."}
        
        try:
            # Agent 실행
            response = self.agent.invoke({
                "messages": [{"role": "user", "content": f"'{query}' 상품을 검색해주세요."}]
            })
            
            # 응답 처리
            result = self._process_response(query, response)
            return result
            
        except Exception as e:
            return {
                "error": f"검색 중 오류가 발생했습니다: {str(e)}",
                "query": query
            }
    
    def _process_response(self, query: str, response: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 응답 처리"""
        try:
            # 메시지에서 최종 AI 응답 추출
            messages = response.get("messages", [])
            if not messages:
                return {"error": "응답을 받지 못했습니다.", "query": query}
            
            # 마지막 AI 메시지 찾기
            ai_message = None
            for msg in reversed(messages):
                if hasattr(msg, 'type') and msg.type == 'ai':
                    ai_message = msg
                    break
                elif isinstance(msg, dict) and msg.get('role') == 'assistant':
                    ai_message = msg
                    break
            
            if not ai_message:
                return {"error": "AI 응답을 찾을 수 없습니다.", "query": query}
            
            # 응답 내용 추출
            if isinstance(ai_message, dict):
                content = ai_message.get('content', '')
            elif hasattr(ai_message, 'content'):
                content = ai_message.content
            else:
                content = str(ai_message)
            
            # 더미 상품 데이터 생성 (실제로는 검색 결과를 파싱해야 함)
            products = self._generate_dummy_products(query, content)
            
            return {
                "query": query,
                "response": content,
                "products": products
            }
            
        except Exception as e:
            return {
                "error": f"응답 처리 중 오류: {str(e)}",
                "query": query
            }
    
    def _generate_dummy_products(self, query: str, search_result: str) -> List[Dict[str, Any]]:
        """더미 상품 데이터 생성"""
        # 검색 쿼리 기반 더미 데이터
        dummy_products = [
            {
                "name": f"{query} 상품 1",
                "description": f"{query}에 대한 검색 결과를 바탕으로 한 상품입니다.",
                "price": "100,000원",
                "rating": "4.5/5",
                "availability": "재고 있음"
            },
            {
                "name": f"{query} 상품 2", 
                "description": f"고품질 {query} 제품입니다.",
                "price": "150,000원",
                "rating": "4.3/5",
                "availability": "재고 있음"
            },
            {
                "name": f"{query} 상품 3",
                "description": f"인기 있는 {query} 브랜드 제품입니다.",
                "price": "200,000원",
                "rating": "4.7/5",
                "availability": "재고 부족"
            }
        ]
        
        return dummy_products