# SalesAssist – 소싱/마진 계산기

네이버·쿠팡 소싱 상품의 마진을 계산하고 엑셀로 내보낼 수 있는 로컬 웹 앱입니다.  
Python + FastAPI 기반이며, 브라우저에서 바로 사용합니다.

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| ⚙️ 비용 설정 | 수수료(%), 배송비, 기타비용, 목표 마진율, **부가세율(%)** 설정 |
| 🧮 빠른 마진 계산기 | 저장 없이 매입가·판매가를 입력하면 즉시 마진 계산 |
| 🔗 키워드·트렌드 바로가기 | 네이버 데이터랩, 쇼핑인사이트, 스마트스토어, 쿠팡Wing, 알리익스프레스 등 한 번에 이동 |
| ➕ 상품 관리 | 상품 추가·수정·삭제 — **소싱처, 소싱 URL** 포함 |
| 📊 마진 색상 표시 | 목표 달성(초록), 절반 이상(노랑), 미달(빨강) |
| 🔄 반품 체크리스트 | 상품별 반품 발생 여부 등록 및 후속 조치(환불·고객연락·재고반영·배송비) 체크리스트 |
| 📥 엑셀 내보내기 | 네이버·쿠팡별 마진 분석 엑셀 다운로드 (소싱처·URL·부가세·반품 현황 포함) |

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

## 🔄 반품 체크리스트 사용법

### 반품 발생 등록 및 후속 조치 체크

상품 목록의 **반품** 열에서 각 상품의 반품 상태를 관리할 수 있습니다.

| 상태 | 표시 | 설명 |
|------|------|------|
| 반품 없음 | `반품 등록` (회색) | 아직 반품이 발생하지 않은 상태 |
| 반품 발생 | `⚠️ 반품 (N/4)` (빨강) | 반품이 발생했으며 후속 처리 진행 중 |

**체크리스트 열기**: 반품 열의 배지를 클릭하면 체크리스트 팝업이 열립니다.

```
┌──────────────────────────────────┐
│ 🔄 반품 체크리스트                │
│ 상품명: 블루투스 이어폰           │
│                                  │
│ [✓] ⚠️ 반품 발생                 │
│                                  │
│ 반품 처리 후속 조치:              │
│ [✓] 💰 환불 완료                 │
│ [ ] 📞 고객 연락                 │
│ [✓] 📦 재고 반영                 │
│ [ ] 🚚 배송비 처리               │
│                                  │
│         [취소]  [저장]           │
└──────────────────────────────────┘
```

### 체크리스트 항목 설명

| 항목 | 설명 |
|------|------|
| ⚠️ 반품 발생 | 해당 상품에 반품이 발생했음을 표시 |
| 💰 환불 완료 | 구매자에게 환불 처리 완료 |
| 📞 고객 연락 | 반품 관련 고객과의 연락 완료 |
| 📦 재고 반영 | 반품된 상품을 재고에 다시 반영 |
| 🚚 배송비 처리 | 반품 배송비 정산/처리 완료 |

### 엑셀 내보내기 시 반품 정보

엑셀 다운로드 시 아래 열이 자동으로 포함됩니다:

- `반품 발생` — `Y` 또는 빈 칸
- `환불 완료`, `고객 연락`, `재고 반영`, `배송비 처리` — 각각 완료 시 `Y`

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
│   └── excel_export.py # 엑셀 내보내기
├── frontend/
│   └── index.html      # 웹 UI
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
다르면:

```bash
git remote set-url origin https://github.com/nadahong99/salesassist.git
```

**4. 패키지 재설치**

```bash
pip install -r requirements.txt
```

---

### ❓ "앱을 실행했는데 브라우저가 안 열려요 / 빈 화면이에요"

```bash
# 직접 실행 확인
python main.py
```

그 다음 브라우저에서 직접 주소 입력: `http://localhost:8000`

포트 충돌이라면 다른 포트 사용:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
# → 브라우저에서 http://localhost:8001 접속
```

---

### ❓ "PR이 아직 열려 있어도 기능이 적용돼 있나요?"

네. **코드가 `main` 브랜치에 있으면** PR 상태와 관계없이 `git pull origin main` 후 바로 사용 가능합니다.

현재 `main` 브랜치에 포함된 기능:

- `main.py` — FastAPI 서버
- `run_app.py` — 윈도우 더블클릭 런처
- `app/models.py` — Config(부가세율 포함), Item(소싱처·URL 포함)
- `app/excel_export.py` — 소싱처·URL·부가세·반품 현황 포함 엑셀 내보내기
- `frontend/index.html` — 빠른 마진 계산기 + 키워드 바로가기 + 상품 관리 + **반품 체크리스트 UI**

```bash
git clone https://github.com/nadahong99/salesassist.git
cd salesassist
pip install -r requirements.txt
python run_app.py
```

위 4줄만 실행하면 바로 됩니다.

---

## 🛠 (선택) EXE 실행파일로 만들기

```bash
pip install pyinstaller
pyinstaller --onefile run_app.py
```

생성된 `dist/run_app.exe` 를 원하는 곳에 두고 더블클릭하면 됩니다.

> ⚠️ EXE 빌드 시 `main.py`, `app/`, `frontend/`, `data/` 폴더를 같은 경로에 함께 두어야 합니다.
