# SalesAssist – 소싱/마진 계산기

네이버·쿠팡 소싱 상품의 마진을 계산하고 엑셀로 내보낼 수 있는 로컬 웹 앱입니다.  
Python + FastAPI 기반이며, 브라우저에서 바로 사용합니다.

---

## ✅ 최신 코드 받기 (git pull)

> **"바뀐 것이 없어요" / "달라진 게 없어요" 라고 느껴질 때 이 단계를 먼저 하세요.**

### 처음 받는 경우 (clone)

```bash
git clone https://github.com/nadahong99/salesassist.git
cd salesassist
```

### 이미 clone 했는데 최신 버전으로 업데이트하고 싶을 때

```bash
# 1. main 브랜치로 이동
git checkout main

# 2. 최신 코드 내려받기
git pull origin main

# 3. (최신 코드로 변경됐으면) 패키지 다시 설치
pip install -r requirements.txt
```

> ⚠️ `git pull` 후에도 변화가 없어 보이면 아래 **🔧 문제 해결** 섹션을 참고하세요.

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

---

## 🔧 문제 해결 (Troubleshooting)

### "git pull 해도 바뀐 게 없어요"

아래 순서로 확인하세요.

**1. 지금 어떤 브랜치에 있는지 확인**

```bash
git branch
```

`* main` 이 표시돼야 합니다. 다른 브랜치에 있으면:

```bash
git checkout main
git pull origin main
```

**2. 원격 저장소 주소 확인**

```bash
git remote -v
```

`https://github.com/nadahong99/salesassist` 가 나와야 합니다.  
다르면: `` git remote set-url origin https://github.com/nadahong99/salesassist.git ``

**3. pull이 진짜 실행됐는지 확인**

```bash
git log --oneline -5
```

최근 커밋 목록이 나옵니다. 가장 위 커밋의 날짜/내용을 GitHub 페이지와 비교해보세요.

**4. 파일이 업데이트됐는지 확인**

```bash
# Windows 명령 프롬프트
dir

# Windows PowerShell / Git Bash
ls -la
```

`main.py`, `run_app.py`, `app/`, `frontend/` 폴더가 모두 보여야 합니다.

**5. 패키지(라이브러리)가 설치됐는지 확인**

```bash
pip install -r requirements.txt
```

이미 설치됐어도 오류 없이 완료됩니다.

---

### "앱을 실행해도 브라우저에 아무것도 안 떠요"

```bash
# 직접 실행 확인
python main.py
```

그 다음 브라우저에서 직접 주소 입력: `http://localhost:8000`

포트 충돌이라면:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
# → 브라우저에서 http://localhost:8001 로 접속
```

---

### "PR이 아직 열려 있는데 코드가 반영이 안 된 건가요?"

아니오. **PR #1 은 아직 열려 있지만, 모든 기능은 이미 `main` 브랜치에 반영되어 있습니다.**  
GitHub에서 PR이 열린(Open) 상태여도 코드가 `main`에 있으면 `git pull origin main` 후 바로 사용 가능합니다.

현재 `main` 브랜치에는 다음이 모두 포함되어 있습니다:

- `main.py` — FastAPI 서버
- `run_app.py` — 윈도우 더블클릭 런처
- `requirements.txt` — 필요 패키지 목록
- `app/` — 모델·저장·엑셀 내보내기 모듈
- `frontend/index.html` — 웹 UI

```bash
git clone https://github.com/nadahong99/salesassist.git
cd salesassist
pip install -r requirements.txt
python run_app.py
```

위 4줄만 실행하면 바로 됩니다.

