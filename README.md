# SalesAssist – 소싱/마진 계산기 v2.0

네이버·쿠팡 소싱 상품의 마진을 계산하고, 세금/영수증 요약 및 엑셀 내보내기를 지원하는 로컬 웹 앱입니다.  
Python + FastAPI 기반이며, 브라우저에서 바로 사용합니다.

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| ⚙️ 비용 설정 | 수수료(%), 배송비, 기타비용, 목표 마진율, **부가세율(%)** 설정 |
| 🧮 빠른 마진 계산기 | 저장 없이 매입가·판매가를 입력하면 즉시 마진 계산 |
| 🧾 세금/영수증 관리 | 총 매입원가·예상 매출·부가세 요약 + 엑셀 영수증 내보내기 |
| 🔗 소싱·키워드·트렌드 바로가기 | 네이버 데이터랩, 쇼핑인사이트, 스마트스토어, 쿠팡Wing, 알리익스프레스 등 한 번에 이동 |
| ➕ 상품 관리 | 상품 추가·수정·삭제 — **소싱처 이름 + 소싱 URL** 포함 |
| 🔗 소싱 URL 바로가기 버튼 | 상품 목록 각 행에 **🔗 바로가기** 버튼으로 소싱 사이트 직접 이동 |
| 📊 마진 색상 표시 | 목표 달성(초록), 절반 이상(노랑), 미달(빨강) |
| 📥 엑셀 내보내기 | 네이버·쿠팡별 마진 분석 엑셀 다운로드 (소싱처·URL·부가세 포함) |

---

## 🚀 설치 및 실행 (윈도우 기준)

### 1. 최초 1회 설치

```bash
git clone https://github.com/nadahong99/salesassist.git
cd salesassist
pip install -r requirements.txt
```

### 2. 앱 실행 (매번)

**방법 A – 더블클릭**

탐색기에서 `run_app.py` 파일을 더블클릭합니다.

**방법 B – 명령 프롬프트**

```bash
python run_app.py
```

실행하면 2초 후 브라우저에서 `http://localhost:8000` 이 자동으로 열립니다.  
종료하려면 이 창에서 **Ctrl+C** 를 누르세요.

---

## 📋 활용 예시

### 예시 1: 상품에 소싱 URL 등록하기

1. **상품 추가** 폼에서:
   - 상품명: `무선 충전 패드`
   - 매입가: `8000`
   - 네이버 판매가: `18900`
   - 소싱처: `알리익스프레스`
   - 소싱 URL: `https://www.aliexpress.com/item/...`
   - **추가** 버튼 클릭

2. **상품 목록**에서 해당 상품 행의 `🔗 바로가기` 버튼을 클릭하면 소싱 사이트로 바로 이동합니다.

3. 소싱 URL은 **수정** 버튼을 눌러 언제든지 변경할 수 있습니다.  
   수정 모달에서 URL 입력 시 미리보기 바로가기 버튼이 즉시 표시됩니다.

---

### 예시 2: 세금/영수증 관리

1. **비용 설정**에서 `부가세율`을 `10`으로 설정하고 저장

2. **세금/영수증 관리** 카드에서 자동으로 계산됩니다:
   - 총 매입 원가: 등록된 모든 상품의 매입가 합계
   - 예상 총 매출 (네이버/쿠팡): 등록된 판매가 합계
   - 예상 부가세: 네이버 매출 × 부가세율

3. `📥 네이버 영수증 엑셀` 또는 `📥 쿠팡 영수증 엑셀` 버튼으로  
   상품별 매입가·판매가·수수료·부가세가 포함된 엑셀 파일을 다운로드합니다.

---

### 예시 3: 마진 계산

1. **비용 설정**에서:
   - 네이버 수수료: `3.5%`
   - 배송비: `3000원`
   - 목표 마진율: `20%`

2. **빠른 마진 계산기**에서 매입가 `8000원`, 판매가 `18900원`, 플랫폼 `네이버` 선택  
   → 마진(원)과 마진율(%)이 즉시 표시됩니다.

3. **상품 목록**의 마진율 셀:
   - 🟢 초록: 목표 마진율 달성
   - 🟡 노랑: 목표의 50% 이상
   - 🔴 빨강: 목표 미달

---

## ✅ 최신 코드 받기 (업데이트)

> **"앱을 실행해도 새 기능이 없어요" / "달라진 게 없어요"** 라면, 먼저 아래 단계를 진행하세요.

```bash
# 1. main 브랜치로 이동
git checkout main

# 2. 최신 코드 받기
git pull origin main

# 3. 패키지 업데이트
pip install -r requirements.txt

# 4. 앱 다시 실행
python run_app.py
```

> ⚠️ 이미 앱이 실행 중이라면 **Ctrl+C** 로 먼저 종료한 후 `git pull` 을 진행하세요.

---

## 📁 프로젝트 구조

```
salesassist/
├── run_app.py          # ← 더블클릭으로 실행하는 런처
├── main.py             # FastAPI 앱 진입점
├── requirements.txt
├── app/
│   ├── models.py       # Pydantic 모델 (Config, Item 등)
│   ├── storage.py      # JSON 데이터 저장
│   └── excel_export.py # 엑셀 내보내기 (부가세/소싱URL 포함)
├── frontend/
│   └── index.html      # 웹 UI (소싱URL 바로가기, 세금요약 등)
├── data/               # 설정/상품 데이터 저장 위치 (자동 생성)
└── output/             # 생성된 엑셀 파일 저장 위치 (자동 생성)
```

---

## 📦 요구사항

- Python 3.10 이상
- 패키지: `fastapi`, `uvicorn[standard]`, `pydantic`, `pandas`, `openpyxl`

---

## 🔧 문제 해결 (Troubleshooting)

### ❓ "run 눌러서 실행했는데 달라진 게 없어요"

VS Code나 PyCharm의 **Run 버튼**으로 실행해도 로컬 코드를 그대로 실행합니다.  
최신 기능을 보려면 먼저 `git pull origin main` 으로 코드를 업데이트해야 합니다.

```
아이디어 적용 순서:
1. git pull origin main   ← 최신 코드를 내려받음
2. pip install -r requirements.txt   ← 혹시 패키지 변경 있으면 반영
3. python run_app.py   ← 다시 실행
```

---

### ❓ "git pull 해도 바뀐 게 없어요"

**1. 지금 어떤 브랜치에 있는지 확인**

```bash
git branch
```

`* main` 이 표시돼야 합니다. 다른 브랜치에 있으면:

```bash
git checkout main
git pull origin main
```

**2. pull이 진짜 실행됐는지 확인**

```bash
git log --oneline -5
```

최근 커밋 목록과 [GitHub 커밋 목록](https://github.com/nadahong99/salesassist/commits/main)을 비교하세요.

**3. 원격 저장소 주소 확인**

```bash
git remote -v
```

`https://github.com/nadahong99/salesassist` 가 나와야 합니다.

**4. 패키지 재설치**

```bash
pip install -r requirements.txt
```

---

### ❓ "앱을 실행했는데 브라우저가 안 열려요 / 빈 화면이에요"

```bash
python main.py
```

그 다음 브라우저에서 직접 주소 입력: `http://localhost:8000`

포트 충돌이라면:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
# → 브라우저에서 http://localhost:8001 접속
```

---

## 🛠 (선택) EXE 실행파일로 만들기

```bash
pip install pyinstaller
pyinstaller --onefile run_app.py
```

생성된 `dist/run_app.exe` 를 원하는 곳에 두고 더블클릭하면 됩니다.

> ⚠️ EXE 빌드 시 `main.py`, `app/`, `frontend/`, `data/` 폴더를 같은 경로에 함께 두어야 합니다.
