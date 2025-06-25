# Vibe Coding W2 - AI 상품 검색 챗봇

## 프로젝트 개요

FastAPI 백엔드와 Streamlit 프론트엔드를 활용한 AI 상품 검색 챗봇 시스템입니다.

## 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 API 프레임워크
- **LangGraph**: AI Agent 구현
- **LangChain**: LLM 통합 및 체인 구성
- **Pydantic**: 데이터 검증 및 직렬화

### 프론트엔드
- **Streamlit**: 대화형 웹 애플리케이션
- **Requests**: HTTP 클라이언트

### 개발 도구
- **pytest**: 테스트 프레임워크
- **GitHub Actions**: CI/CD 자동화
- **pre-commit**: 코드 품질 관리

## 프로젝트 구조

```
vibe_coding_w2/
│
├── backend/                 # 백엔드 코드
│   ├── __init__.py
│   ├── main.py             # FastAPI 애플리케이션
│   ├── agent.py            # AI Agent 구현
│   └── config.py           # 설정 관리
│
├── frontend/               # 프론트엔드 코드
│   └── app.py              # Streamlit 애플리케이션
│
├── tests/                  # 테스트 코드
│   ├── test_backend.py
│   ├── test_frontend.py
│   ├── test_agent.py
│   └── test_project_structure.py
│
├── docs/                   # 문서
│   ├── ux-wireframes.md
│   └── chat-interface-wireframe.svg
│
├── .cursor/                # Cursor IDE 설정
│   └── rules/              # 개발 규칙
│
├── .github/                # GitHub 설정
│   ├── workflows/          # GitHub Actions
│   ├── ISSUE_TEMPLATE/     # 이슈 템플릿
│   ├── CODEOWNERS          # 코드 소유자
│   └── pull_request_template.md
│
├── requirements.txt        # Python 의존성
├── .gitignore             # Git 무시 파일
└── README.md              # 프로젝트 문서
```

## 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/visvaden7/vibe_coding_w2.git
cd vibe_coding_w2
```

### 2. 가상환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 필요한 API 키를 설정하세요:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. 백엔드 실행

```bash
python -m uvicorn backend.main:app --reload
```

### 6. 프론트엔드 실행

새 터미널에서:

```bash
streamlit run frontend/app.py
```

## 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 테스트 실행
pytest --cov=backend --cov=frontend

# 특정 테스트 파일 실행
pytest test_backend.py
```

## API 문서

백엔드 서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 주요 기능

### 🤖 AI Agent
- LangGraph 기반 대화형 AI Agent
- 상품 검색 및 추천 기능
- 컨텍스트 인식 대화

### 🌐 웹 인터페이스
- 실시간 채팅 인터페이스
- 스트리밍 응답 표시
- 반응형 UI 디자인

### 🔧 자동화
- GitHub Actions 기반 CI/CD
- 자동 테스트 실행
- PR/이슈 자동 관리
- 코드 품질 검사

## 개발 워크플로우

### 1. 기능 개발
1. 새 브랜치 생성: `git checkout -b feature/새기능`
2. 테스트 코드 작성 (TDD)
3. 기능 구현
4. 테스트 통과 확인
5. PR 생성

### 2. 코드 리뷰
- GitHub Actions이 자동으로 테스트 실행
- 자동 라벨링 및 리뷰어 할당
- 코드 품질 검사 및 리뷰 코멘트 생성

### 3. 배포
- main 브랜치 병합 시 자동 배포
- 테스트 통과 후에만 배포 진행

## 기여하기

1. 이 저장소를 포크하세요
2. 새 기능 브랜치를 만드세요 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/AmazingFeature`)
5. Pull Request를 열어주세요

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

---

**개발자**: visvaden7  
**프로젝트 링크**: https://github.com/visvaden7/vibe_coding_w2