# SalesAssist – 소싱/마진 계산기

네이버·쿠팡 소싱 상품의 마진을 계산하고 엑셀로 내보낼 수 있는 로컬 웹 앱입니다.  
Python + FastAPI 기반이며, 브라우저에서 바로 사용합니다.

---

## 🚀 윈도우에서 제일 편한 사용 방법

### 1. 최초 1회 설치

```bash
pip install -r requirements.txt
```

### 2. 앱 실행 (매번)

**방법 A – 더블클릭**

탐색기에서 `run_app.py` 파일을 더블클릭합니다.

**방법 B – 명령 프롬프트**

```bash
python run_app.py
```

실행하면:

1. 서버가 자동으로 시작됩니다.
2. 2초 후 기본 브라우저에서 `http://localhost:8000` 이 열립니다.
3. 앱을 다 쓰고 나면 이 창에서 **Ctrl+C** 를 누르거나 창을 닫으면 서버가 종료됩니다.

---

## ✨ 주요 기능

- **비용 설정**: 수수료(%), 배송비, 기타비용, 목표 마진율 설정
- **상품 관리**: 상품 추가/수정/삭제
- **마진 색상 표시**: 목표 달성(초록), 절반 이상(노랑), 미달(빨강)
- **엑셀 내보내기**: 네이버/쿠팡별 마진 분석 엑셀 파일 다운로드

---

## 📁 프로젝트 구조

```
salesassist/
├── run_app.py          # ← 더블클릭으로 실행하는 런처
├── main.py             # FastAPI 앱 진입점
├── requirements.txt
├── app/
│   ├── models.py       # Pydantic 모델
│   ├── storage.py      # JSON 데이터 저장
│   └── excel_export.py # 엑셀 내보내기
├── frontend/
│   └── index.html      # 웹 UI
├── data/               # 설정/상품 데이터 저장 위치
└── output/             # 생성된 엑셀 파일 저장 위치
```

---

## 🛠 (선택) EXE 실행파일로 만들기

매번 Python 없이 `run_app.exe` 하나만 더블클릭해서 쓰고 싶다면:

```bash
pip install pyinstaller
pyinstaller --onefile run_app.py
```

생성된 `dist/run_app.exe` 를 원하는 곳에 두고 더블클릭하면 됩니다.

> ⚠️ EXE 빌드 시 `main.py`, `app/`, `frontend/`, `data/` 폴더를 같은 경로에 함께 두어야 합니다.

---

## 📦 요구사항

- Python 3.10 이상
- 패키지: `fastapi`, `uvicorn[standard]`, `pydantic`, `pandas`, `openpyxl`
