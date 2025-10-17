# 📱 모바일 최적화 가이드

## 🎯 개요

Streamlit 대시보드를 모바일 브라우저에서 최적화하여 사용하기 위한 가이드입니다.

---

## 🐛 일반적인 모바일 문제점

### 1. 차트가 깨짐
- **원인**: 차트 크기가 화면 너비를 초과
- **증상**: 차트가 잘리거나 스크롤이 생김

### 2. 텍스트가 작음
- **원인**: 데스크톱용 폰트 크기 사용
- **증상**: 글자를 읽기 어려움

### 3. 사이드바가 보이지 않음
- **원인**: 모바일에서 사이드바가 자동으로 숨겨짐
- **증상**: 필터 옵션 접근 불가

### 4. KPI 카드가 세로로 길게 늘어남
- **원인**: 반응형 그리드가 1열로 변경됨
- **증상**: 스크롤이 너무 길어짐

### 5. 버튼이 너무 작음
- **원인**: 터치 타겟 크기 부족
- **증상**: 버튼 클릭이 어려움

---

## ✅ 모바일 최적화 개선 사항

### 1. 반응형 CSS 추가

`app.py`의 CSS 섹션에 모바일 전용 스타일 추가:

```python
# 커스텀 CSS (라인 37-72)
st.markdown(f"""
<style>
    /* 기존 CSS... */
    
    /* 모바일 최적화 CSS 추가 */
    @media (max-width: 768px) {{
        /* 메인 타이틀 크기 조정 */
        h1 {{
            font-size: 24px !important;
        }}
        
        h2 {{
            font-size: 18px !important;
        }}
        
        h3 {{
            font-size: 16px !important;
        }}
        
        /* 메트릭 카드 간격 조정 */
        .stMetric {{
            padding: 10px !important;
            margin-bottom: 10px;
        }}
        
        .stMetric label {{
            font-size: 12px !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            font-size: 18px !important;
        }}
        
        /* 버튼 크기 증가 (터치 타겟) */
        .stButton button {{
            min-height: 44px !important;
            font-size: 14px !important;
        }}
        
        /* 차트 컨테이너 */
        .js-plotly-plot {{
            width: 100% !important;
        }}
        
        /* 테이블 폰트 크기 */
        .dataframe {{
            font-size: 12px !important;
        }}
        
        /* 사이드바 */
        [data-testid="stSidebar"] {{
            width: 280px !important;
        }}
        
        /* 컨테이너 패딩 */
        .main .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }}
    }}
    
    /* 작은 모바일 (360px 이하) */
    @media (max-width: 360px) {{
        h1 {{
            font-size: 20px !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            font-size: 16px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)
```

### 2. 차트 높이 동적 조정

차트 생성 시 `height` 파라미터를 화면 크기에 따라 조정:

```python
# analyzers 모듈의 차트 생성 함수에서
import streamlit as st

# 모바일 체크 (간단한 방법)
def get_chart_height():
    """화면 크기에 따른 차트 높이 반환"""
    # Streamlit은 기본적으로 반응형이므로
    # 모바일에서는 작은 높이 사용
    return 400  # 데스크톱: 400-500, 모바일: 300-350

layout.update({
    'height': get_chart_height()
})
```

### 3. 컬럼 레이아웃 조건부 설정

모바일에서는 1열, 데스크톱에서는 2열 사용:

```python
# display_product_section 함수 수정 예시
def display_product_section(product_analyzer):
    """제품 분석 섹션을 표시합니다."""
    st.header("📦 제품 분석")
    
    # 차트 표시 (use_container_width=True 사용)
    st.plotly_chart(
        product_analyzer.create_category_pie_chart(),
        use_container_width=True,  # 이것이 핵심!
        key="category_pie"
    )
    
    st.plotly_chart(
        product_analyzer.create_category_bar_chart(),
        use_container_width=True,
        key="category_bar"
    )
```

### 4. 사이드바 안내 메시지

모바일 사용자를 위한 안내 추가:

```python
# main() 함수 시작 부분에 추가
st.sidebar.info("📱 모바일 사용 팁: 좌측 상단 '>' 버튼으로 메뉴를 열고 닫을 수 있습니다.")
```

### 5. 데이터 테이블 최적화

모바일에서 테이블이 너무 넓을 때:

```python
# display_product_section에서
st.subheader("제품 분류별 TOP 3 매출")
top_products = product_analyzer.get_top_products_by_category(3)
top_products_display = top_products.copy()

# 모바일을 위해 컬럼 줄이기
top_products_display = top_products_display[['분류명', '제품명', '매출액']]
top_products_display['매출액'] = top_products_display['매출액'].apply(lambda x: f"₩{x/10000:.0f}만")

st.dataframe(
    top_products_display, 
    use_container_width=True,
    hide_index=True,
    height=300  # 높이 제한
)
```

---

## 🔧 즉시 적용 가능한 개선

### 1. `use_container_width=True` 추가

모든 `st.plotly_chart()` 호출에 추가:

```python
# 변경 전
st.plotly_chart(fig)

# 변경 후
st.plotly_chart(fig, use_container_width=True)
```

### 2. 차트 config 설정

모바일 터치 최적화:

```python
# analyzers의 각 차트 생성 함수에서
config = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'zoom2d'],
    'locale': 'ko',
    'responsive': True  # 반응형 활성화
}
```

### 3. Plotly 차트 레이아웃 개선

```python
# config.py의 PLOTLY_LAYOUT에 추가
PLOTLY_LAYOUT = {
    # ... 기존 설정 ...
    'autosize': True,  # 자동 크기 조정
    'responsive': True,  # 반응형
    'margin': {'l': 40, 'r': 20, 't': 40, 'b': 40},  # 여백 축소
}
```

---

## 📊 모바일 테스트 방법

### 1. Chrome DevTools 사용

1. Chrome 브라우저에서 `F12` 키
2. 좌측 상단 **"Toggle device toolbar"** (Ctrl+Shift+M)
3. 디바이스 선택:
   - iPhone SE (375x667)
   - iPhone 12 Pro (390x844)
   - Pixel 5 (393x851)
   - Samsung Galaxy S20 (360x800)

### 2. 실제 모바일 기기 테스트

```bash
# 로컬 네트워크에서 접근 가능하게 실행
streamlit run app.py --server.address 0.0.0.0
```

스마트폰에서 `http://YOUR_PC_IP:8501` 접속

### 3. Streamlit Cloud 배포 후 테스트

Streamlit Cloud에 배포하면 공개 URL로 모바일에서 바로 테스트 가능

---

## 🎨 권장 모바일 UI 패턴

### 1. 차트는 세로 스크롤

2열 → 1열로 자동 변경되도록 `st.columns()`를 조건부로 사용하지 않고,
Streamlit의 자동 반응형을 활용

### 2. KPI 카드 간소화

모바일에서는 메인 KPI만 표시:

```python
# 모바일 버전 (선택사항)
col1, col2 = st.columns(2)
with col1:
    st.metric("총 매출", "₩1.2억")
with col2:
    st.metric("거래건수", "1,802건")
```

### 3. 탭 활용

긴 페이지 대신 탭으로 구분 (이미 적용됨 ✅)

---

## 🚀 즉시 적용 체크리스트

- [ ] 모든 차트에 `use_container_width=True` 추가
- [ ] 모바일 전용 CSS 미디어 쿼리 추가
- [ ] 차트 높이를 400px 이하로 조정
- [ ] 사이드바에 모바일 안내 메시지 추가
- [ ] Plotly config에 `responsive: True` 추가
- [ ] 테이블 컬럼 수 줄이기 (모바일에서)
- [ ] 버튼 최소 높이 44px 이상 설정
- [ ] 폰트 크기 확인 (최소 12px)
- [ ] Chrome DevTools로 테스트
- [ ] 실제 모바일 기기에서 테스트

---

## 💡 추가 팁

### 1. 로딩 속도 최적화

```python
# 데이터 캐싱 (이미 적용됨)
@st.cache_data
def load_data():
    # ...
```

### 2. 이미지 최적화

차트를 PNG로 저장할 때 해상도 조정:

```python
config = {
    'toImageButtonOptions': {
        'format': 'png',
        'width': 800,
        'height': 600,
        'scale': 2  # Retina 디스플레이 대응
    }
}
```

### 3. 프로그레스 바 추가

모바일에서는 로딩이 길게 느껴지므로:

```python
with st.spinner('데이터를 분석하는 중...'):
    # 분석 작업
```

---

## 📚 참고 자료

- [Streamlit 공식 문서 - Layouts](https://docs.streamlit.io/library/api-reference/layout)
- [Plotly 반응형 차트](https://plotly.com/python/responsive-plots/)
- [모바일 웹 디자인 가이드](https://web.dev/responsive-web-design-basics/)

---

## 🆘 문제 해결

### 문제: 사이드바가 안 보임
**해결**: 좌측 상단 햄버거 메뉴(≡) 클릭

### 문제: 차트가 여전히 깨짐
**해결**: `use_container_width=True` 확인

### 문제: 텍스트가 작음
**해결**: 모바일 CSS 미디어 쿼리 추가

### 문제: 로딩이 느림
**해결**: 데이터 캐싱 및 필터링 최적화

---

**버전**: v1.0  
**최종 수정일**: 2025년 10월 17일  
**작성자**: 데이터 분석팀

