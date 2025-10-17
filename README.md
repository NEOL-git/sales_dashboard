# 판매 데이터 분석 시스템 (HTML 보고서 + Streamlit 대시보드)

판매 데이터(Excel)를 분석하여 **HTML 보고서** 또는 **Streamlit 인터랙티브 대시보드**를 생성하는 Python 기반 시스템입니다.

## 🎯 두 가지 사용 방법

### 방법 1: Streamlit 인터랙티브 대시보드 (추천) ⭐

실시간으로 데이터를 필터링하고 분석할 수 있는 웹 기반 대시보드

### 방법 2: HTML 정적 보고서

PDF 저장이 가능한 정적 HTML 보고서 생성

---

## 📋 주요 기능

### Streamlit 대시보드 기능
- **📁 Excel/CSV 파일 업로드**: 사용자의 데이터 파일 직접 업로드 및 분석 ⭐ 신규!
  - Excel (.xlsx, .xls) 지원
  - CSV (.csv) 지원 - 자동 인코딩 감지
- **실시간 데이터 필터링**: 날짜, 제품 분류, 거래처별 필터링
- **인터랙티브 차트**: Plotly 기반 동적 차트
- **탭 기반 네비게이션**: 섹션별 구분된 UI
- **반응형 디자인**: 데스크톱/태블릿 자동 대응
- **자동 새로고침**: 데이터 변경 시 즉시 반영

### HTML 보고서 기능
- **자동화된 보고서 생성**: 원클릭 실행
- **PDF 저장 가능**: 브라우저에서 인쇄/저장
- **전문적인 디자인**: 디자인 가이드 준수

---

## 📊 보고서 구성

### 1. 대시보드 개요 (KPI)
- 총 매출액, 거래 건수, 평균 거래 금액
- 총 할인액, 거래처 수
- 평균 할인율, 총 판매 수량, 제품 종류

### 2. 시계열 분석
- 월별 매출 추이 (라인 차트)
- 월별 거래 건수 추이
- 분기별 매출 비교
- 요일별 판매 패턴

### 3. 제품 분석
- 제품 분류별 매출 비중 (파이 차트)
- 제품 분류별 매출액 순위 (바 차트)
- 제품 분류별 TOP 3 매출 (테이블)
- 단가대별 제품 분포

### 4. 거래처 분석
- 거래처별 매출액 TOP 10
- 거래처별 거래 건수
- 주요 거래처 상세 정보 (테이블)

### 5. 할인 분석
- 할인 적용 vs 정상가 거래 비교
- 할인율별 매출 분포
- 제품 분류별 평균 할인율

---

## 🚀 시작하기

### 필수 요구사항

- **Python 3.8 이상**
- **판매 데이터 Excel 파일** (`판매.xlsx`)

### 설치 방법

1. 필요한 라이브러리 설치:

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install pandas openpyxl numpy plotly jinja2 streamlit
```

---

## 💻 사용 방법

### ⭐ **방법 A: Streamlit 대시보드 실행 (추천)**

```bash
streamlit run app.py
```

실행 후 브라우저에서 자동으로 `http://localhost:8501` 열림

#### Streamlit 대시보드 특징:
- 📁 **파일 업로드**: Excel 파일 직접 업로드하여 분석 ⭐ 신규!
- 🔍 **사이드바 필터**: 날짜, 제품 분류, 거래처별 필터링
- 📊 **실시간 분석**: 필터 적용 시 즉시 차트 업데이트
- 📑 **탭 네비게이션**: 5개 섹션을 탭으로 구분
- 💾 **데이터 캐싱**: 빠른 로딩 속도

#### 파일 업로드 사용법:
1. 브라우저에서 대시보드 열기
2. 사이드바 상단 **"📁 데이터 소스"** 섹션
3. **"Browse files"** 클릭하여 Excel 또는 CSV 파일 업로드
4. 자동으로 분석 시작 및 모든 차트 업데이트

**지원 형식**:
- Excel: `.xlsx`, `.xls`
- CSV: `.csv` (UTF-8, CP949, EUC-KR 등 자동 감지)

---

### 방법 B: HTML 정적 보고서 생성

#### 1. 배치 파일 실행 (Windows)
`generate_report.bat` 파일을 더블클릭

#### 2. Python 명령어 실행
```bash
python generate_report.py
```

또는

```bash
py -3 generate_report.py
```

생성된 보고서는 `output/` 폴더에 저장됩니다.

---

## 📁 파일 구조

```
Sales_Dashboard_streamlit/
├── 판매.xlsx                      # 원본 데이터 (매월 업데이트)
│
├── app.py                         # ⭐ Streamlit 대시보드 메인 파일
├── generate_report.py            # HTML 보고서 생성 스크립트
├── generate_report.bat           # 원클릭 실행 파일 (Windows)
│
├── requirements.txt              # 필요 라이브러리 목록
├── config.py                     # 디자인 설정 (색상, 폰트 등)
├── data_loader.py                # 데이터 로딩 모듈
├── report_generator.py           # HTML 보고서 생성 모듈
│
├── analyzers/                    # 분석 모듈 디렉토리
│   ├── __init__.py
│   ├── kpi_analyzer.py          # KPI 분석
│   ├── timeseries_analyzer.py   # 시계열 분석
│   ├── product_analyzer.py      # 제품 분석
│   ├── customer_analyzer.py     # 거래처 분석
│   └── discount_analyzer.py     # 할인 분석
│
├── output/                       # 생성된 HTML 보고서 저장 폴더
│   └── sales_report_YYYYMMDD_HHMMSS.html
│
├── 보고서_구성안.md              # 보고서 구성 문서
├── 보고서 디자인 가이드.md       # 디자인 가이드
└── README.md                     # 본 문서
```

---

## 🎨 디자인 가이드

보고서는 `보고서 디자인 가이드.md`에 정의된 디자인 원칙을 따릅니다:

### 색상 팔레트

- **Primary Blue** (#0A5CA4): 강조 요소, 주요 차트
- **Secondary Blue** (#5DA8D4): 보조 요소
- **Light Blue** (#A9CCE3): 배경 및 보조 차트
- **Neutral Gray** (#D9D9D9): 테두리, 배경
- **Dark Gray** (#333333): 텍스트

### 폰트

- 제목: Arial, Segoe UI, 맑은 고딕 (20-24pt, Bold)
- 본문: Arial, Segoe UI, 맑은 고딕 (10-12pt, Regular)

---

## 🔧 커스터마이징

### 색상 및 디자인 변경

`config.py` 파일에서 색상 팔레트와 폰트 설정을 변경할 수 있습니다.

```python
COLORS = {
    'primary_blue': '#0A5CA4',
    'secondary_blue': '#5DA8D4',
    # ... 더 많은 색상 설정
}
```

### 분석 모듈 수정

각 분석 모듈은 독립적으로 작동하므로 개별 수정이 가능합니다:

- **KPI 수정**: `analyzers/kpi_analyzer.py`
- **시계열 분석 수정**: `analyzers/timeseries_analyzer.py`
- **제품 분석 수정**: `analyzers/product_analyzer.py`
- **거래처 분석 수정**: `analyzers/customer_analyzer.py`
- **할인 분석 수정**: `analyzers/discount_analyzer.py`

### Streamlit 대시보드 수정

`app.py` 파일을 수정하여 레이아웃, 필터, UI를 커스터마이징할 수 있습니다.

### HTML 보고서 레이아웃 수정

`report_generator.py` 파일의 HTML 템플릿을 수정하여 보고서 레이아웃을 변경할 수 있습니다.

---

## 📝 데이터 형식

### 필수 컬럼

Excel 파일은 다음 컬럼을 포함해야 합니다:

- `날짜`: 거래 날짜 (날짜 형식)
- `거래처명`: 거래처 이름 (텍스트)
- `분류명`: 제품 분류 (텍스트)
- `제품명`: 제품 이름 (텍스트)
- `단가`: 제품 단가 (숫자)
- `수량`: 판매 수량 (숫자)
- `금액`: 총 금액 (숫자)

### 선택 컬럼

- `Discount`: 할인율 (0~1 사이의 소수)
- `색상`: 제품 색상 (텍스트)
- `제품코드`: 제품 코드 (텍스트)

---

## 🔄 데이터 업데이트

### Streamlit 대시보드 사용 시:
1. 새로운 판매 데이터를 `판매.xlsx` 파일에 업데이트
2. 브라우저에서 "Always rerun" 선택 또는 'R' 키 눌러 새로고침
3. 실시간으로 업데이트된 데이터 확인

### HTML 보고서 사용 시:
1. 새로운 판매 데이터를 `판매.xlsx` 파일에 업데이트
2. `generate_report.bat` 실행 또는 `python generate_report.py` 실행
3. `output/` 폴더에서 생성된 보고서 확인

---

## 🐛 문제 해결

### 모듈을 찾을 수 없다는 오류

```bash
pip install -r requirements.txt
```

### Excel 파일을 읽을 수 없다는 오류

- Excel 파일이 닫혀 있는지 확인
- 파일명이 `판매.xlsx`인지 확인
- 시트명이 `Sheet1` 또는 `판매`인지 확인

### Streamlit 실행 오류

```bash
# Streamlit 재설치
pip uninstall streamlit
pip install streamlit

# 캐시 삭제
streamlit cache clear
```

### 차트가 표시되지 않는 오류

- 인터넷 연결 확인 (Plotly CDN 사용)
- 브라우저의 JavaScript가 활성화되어 있는지 확인

### 포트가 이미 사용 중이라는 오류

```bash
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

---

## 🆚 Streamlit vs HTML 보고서 비교

| 기능 | Streamlit 대시보드 | HTML 보고서 |
|------|-------------------|------------|
| 인터랙티브 필터 | ✅ | ❌ |
| 실시간 업데이트 | ✅ | ❌ |
| PDF 저장 | ⚠️ (브라우저 인쇄) | ✅ |
| 오프라인 사용 | ❌ (서버 필요) | ✅ |
| 배포 | Streamlit Cloud | 파일 공유 |
| 사용 편의성 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### 추천 사용 시나리오:

- **Streamlit 대시보드**: 일상적인 데이터 분석, 팀 내부 공유, 실시간 의사결정
- **HTML 보고서**: 공식 보고서 제출, PDF 저장 필요, 오프라인 공유

---

## 💡 추가 기능 (향후 개발)

- [x] ~~Streamlit 인터랙티브 대시보드~~
- [x] ~~실시간 필터링 기능~~
- [x] ~~Excel 파일 업로드 기능 (Streamlit)~~ ⭐ 완료!
- [x] ~~CSV 파일 지원~~ ⭐ 완료!
- [ ] 전월 대비 증감률 표시
- [ ] 데이터 백업 기능
- [ ] 다중 파일 비교 분석
- [ ] 이상치 자동 감지 및 하이라이트
- [ ] 다국어 지원 (영문)
- [ ] Streamlit Cloud 배포 가이드

---

## 📞 문의

데이터 분석 및 보고서 관련 문의사항이 있으시면 데이터 분석팀으로 연락 주시기 바랍니다.

---

## 🎓 참고 문서

- [보고서 구성안](./보고서_구성안.md)
- [보고서 디자인 가이드](./보고서%20디자인%20가이드.md)
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Plotly 공식 문서](https://plotly.com/python/)

---

**버전**: v2.2 (CSV 파일 지원 추가)  
**작성일**: 2025년 10월 15일  
**최종 수정일**: 2025년 10월 17일  
**주요 변경사항**: 
- v2.2: CSV 파일 업로드 지원 (자동 인코딩 감지)
- v2.1: Excel 파일 업로드 기능 추가
- v2.0: Streamlit 인터랙티브 대시보드 추가
