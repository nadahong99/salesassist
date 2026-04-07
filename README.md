# SalesAssist – 소싱 & 마진 관리 도구

네이버 스마트스토어 / 쿠팡 재판매를 위한 **로컬 전용** 소싱 상품 관리 및 마진 계산 웹앱입니다.  
AI 없이 동작하며, 모든 데이터는 로컬 JSON 파일에 저장됩니다.

---

## 요구 사항

- **OS**: Windows (Mac/Linux에서도 동작)
- **Python**: 3.10 이상
- 인터넷 연결: 최초 패키지 설치 시에만 필요

---

## 설치 & 실행

```bat
git clone https://github.com/nadahong99/salesassist.git
cd salesassist
pip install -r requirements.txt
python main.py
```

브라우저에서 [http://localhost:8000](http://localhost:8000) 접속.

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| **수수료 설정** | 네이버/쿠팡 수수료율, 기타비용(포장·배송) 저장 |
| **상품 관리** | 소싱 상품 추가·수정·삭제 (상품명, 원가, 판매가, 소싱처, URL, 옵션, 메모) |
| **마진율 표시** | 네이버·쿠팡 마진율 자동 계산 후 색상으로 표시 (🔴<10% / 🟡10~20% / 🟢≥20%) |
| **엑셀 내보내기** | 네이버용·쿠팡용 xlsx 파일 다운로드 (`output/` 폴더에도 저장) |

---

## 마진 계산 공식

```
total_cost   = 원가 + 기타비용
fee          = 판매가 × 수수료율
margin       = 판매가 − total_cost − fee
margin_rate  = margin / 판매가 × 100  (판매가 > 0 인 경우)
```

---

## 파일 구조

```
salesassist/
├── main.py              # FastAPI 앱 진입점
├── requirements.txt
├── app/
│   ├── models.py        # Pydantic 모델
│   ├── storage.py       # JSON 읽기/쓰기
│   └── excel_export.py  # 엑셀 생성
├── frontend/
│   ├── index.html
│   ├── main.js
│   └── styles.css
├── data/
│   ├── config.json      # 수수료 설정 (자동 생성)
│   └── items.json       # 상품 목록 (자동 생성)
└── output/              # 생성된 엑셀 파일 저장
```

---

## 데이터 초기화

`data/` 폴더 및 JSON 파일은 앱 첫 실행 시 자동으로 생성됩니다.  
수동으로 초기화하려면 `data/items.json` 내용을 `[]`로 변경하면 됩니다.
