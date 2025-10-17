#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
판매 데이터 분석 Streamlit 대시보드

실행 방법:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys

# 모듈 임포트
from data_loader import SalesDataLoader
from analyzers import (
    KPIAnalyzer,
    TimeSeriesAnalyzer,
    ProductAnalyzer,
    CustomerAnalyzer,
    DiscountAnalyzer
)
from config import COLORS, REPORT_CONFIG


# 페이지 설정
st.set_page_config(
    page_title="판매 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown(f"""
<style>
    .main {{
        background-color: {COLORS['white']};
    }}
    .stMetric {{
        background-color: {COLORS['light_gray']};
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {COLORS['primary_blue']};
    }}
    .stMetric label {{
        color: {COLORS['dark_gray']};
        font-size: 14px;
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: {COLORS['primary_blue']};
        font-size: 24px;
        font-weight: bold;
    }}
    h1 {{
        color: {COLORS['primary_blue']};
    }}
    h2 {{
        color: {COLORS['primary_blue']};
        border-bottom: 2px solid {COLORS['primary_blue']};
        padding-bottom: 10px;
    }}
    h3 {{
        color: {COLORS['dark_gray']};
    }}
    .sidebar .sidebar-content {{
        background-color: {COLORS['light_gray']};
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data_from_file(file_path, sheet_name='Sheet1'):
    """파일 경로로부터 데이터를 로드하고 캐싱합니다."""
    loader = SalesDataLoader(file_path, sheet_name)
    df = loader.load_data()
    
    if not loader.validate_data():
        st.error("❌ 데이터 검증 실패")
        st.stop()
    
    data_info = loader.get_data_info()
    return df, data_info


def load_data_from_upload(uploaded_file, sheet_name='Sheet1'):
    """업로드된 파일로부터 데이터를 로드합니다. (Excel 및 CSV 지원)"""
    try:
        # 파일 확장자 확인
        file_name = uploaded_file.name
        file_extension = file_name.split('.')[-1].lower()
        
        # 파일 형식에 따라 읽기
        if file_extension == 'csv':
            # CSV 파일 읽기 (여러 인코딩 시도)
            encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
            df = None
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)  # 파일 포인터 초기화
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    st.sidebar.success(f"✅ CSV 인코딩: {encoding.upper()}")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                st.error("❌ CSV 파일의 인코딩을 인식할 수 없습니다.")
                st.info("💡 파일을 UTF-8 형식으로 저장한 후 다시 시도해보세요.")
                return None, None
        elif file_extension in ['xlsx', 'xls']:
            # Excel 파일 읽기
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        else:
            st.error(f"⚠️ 지원하지 않는 파일 형식: .{file_extension}")
            st.info("📋 지원 형식: Excel (.xlsx, .xls) 또는 CSV (.csv)")
            return None, None
        
        # 컬럼명 정리 (공백 제거)
        df.columns = df.columns.str.strip()
        
        # 날짜 컬럼을 datetime으로 변환
        if '날짜' in df.columns:
            df['날짜'] = pd.to_datetime(df['날짜'])
        
        # 파생 컬럼 생성 (data_loader와 동일한 로직)
        if '날짜' in df.columns:
            df['년'] = df['날짜'].dt.year
            df['월'] = df['날짜'].dt.month
            df['분기'] = df['날짜'].dt.quarter
            df['요일'] = df['날짜'].dt.day_name()
            df['년월'] = df['날짜'].dt.to_period('M').astype(str)
            
            요일_매핑 = {
                'Monday': '월요일',
                'Tuesday': '화요일',
                'Wednesday': '수요일',
                'Thursday': '목요일',
                'Friday': '금요일',
                'Saturday': '토요일',
                'Sunday': '일요일'
            }
            df['요일명'] = df['요일'].map(요일_매핑)
        
        if 'Discount' in df.columns:
            df['할인율'] = df['Discount'] * 100
        
        if '단가' in df.columns and '수량' in df.columns and 'Discount' in df.columns:
            df['할인전금액'] = df['단가'] * df['수량']
            df['할인액'] = df['할인전금액'] * df['Discount']
        
        if 'Discount' in df.columns:
            df['할인적용'] = df['Discount'].apply(lambda x: '할인' if x > 0 else '정상가')
        
        # 데이터 정보 수집
        data_info = {
            '총_거래건수': len(df),
            '데이터_시작일': df['날짜'].min() if '날짜' in df.columns else None,
            '데이터_종료일': df['날짜'].max() if '날짜' in df.columns else None,
            '컬럼_목록': list(df.columns),
            '거래처_수': df['거래처명'].nunique() if '거래처명' in df.columns else 0,
            '제품_수': df['제품명'].nunique() if '제품명' in df.columns else 0,
            '제품분류_수': df['분류명'].nunique() if '분류명' in df.columns else 0,
        }
        
        # 데이터 검증
        required_columns = ['날짜', '거래처명', '분류명', '제품명', '단가', '수량', '금액']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"⚠️ 필수 컬럼 누락: {', '.join(missing_columns)}")
            st.info("📋 필수 컬럼: 날짜, 거래처명, 분류명, 제품명, 단가, 수량, 금액")
            return None, None
        
        return df, data_info
    
    except Exception as e:
        st.error(f"❌ 파일 로드 중 오류 발생: {e}")
        return None, None


def filter_data(df, date_range, categories, customers):
    """데이터를 필터링합니다."""
    filtered_df = df.copy()
    
    # 날짜 필터
    if date_range:
        filtered_df = filtered_df[
            (filtered_df['날짜'] >= pd.Timestamp(date_range[0])) &
            (filtered_df['날짜'] <= pd.Timestamp(date_range[1]))
        ]
    
    # 제품 분류 필터
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['분류명'].isin(categories)]
    
    # 거래처 필터
    if customers and len(customers) > 0:
        filtered_df = filtered_df[filtered_df['거래처명'].isin(customers)]
    
    return filtered_df


def display_kpi_section(kpis):
    """KPI 대시보드 섹션을 표시합니다."""
    st.header("📊 대시보드 개요")
    
    # 메인 KPI
    col1, col2, col3, col4 = st.columns(4)
    
    main_kpis = kpis['main_kpis']
    
    with col1:
        st.metric(
            label=main_kpis[0]['label'],
            value=main_kpis[0]['formatted']
        )
    
    with col2:
        st.metric(
            label=main_kpis[1]['label'],
            value=main_kpis[1]['formatted']
        )
    
    with col3:
        st.metric(
            label=main_kpis[2]['label'],
            value=main_kpis[2]['formatted']
        )
    
    with col4:
        st.metric(
            label=main_kpis[3]['label'],
            value=main_kpis[3]['formatted']
        )
    
    st.markdown("---")
    
    # 서브 KPI
    col5, col6, col7, col8 = st.columns(4)
    
    sub_kpis = kpis['sub_kpis']
    
    with col5:
        st.metric(
            label=sub_kpis[0]['label'],
            value=sub_kpis[0]['formatted']
        )
    
    with col6:
        st.metric(
            label=sub_kpis[1]['label'],
            value=sub_kpis[1]['formatted']
        )
    
    with col7:
        st.metric(
            label=sub_kpis[2]['label'],
            value=sub_kpis[2]['formatted']
        )
    
    with col8:
        st.metric(
            label=sub_kpis[3]['label'],
            value=sub_kpis[3]['formatted']
        )


def display_timeseries_section(timeseries_analyzer):
    """시계열 분석 섹션을 표시합니다."""
    st.header("📈 시계열 분석")
    
    # 월별 매출 추이
    st.plotly_chart(
        timeseries_analyzer.create_monthly_sales_chart(),
        use_container_width=True,
        key="monthly_sales"
    )
    
    # 2열 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            timeseries_analyzer.create_monthly_transactions_chart(),
            use_container_width=True,
            key="monthly_transactions"
        )
    
    with col2:
        st.plotly_chart(
            timeseries_analyzer.create_quarterly_sales_chart(),
            use_container_width=True,
            key="quarterly_sales"
        )
    
    # 요일별 패턴
    st.plotly_chart(
        timeseries_analyzer.create_weekday_chart(),
        use_container_width=True,
        key="weekday"
    )


def display_product_section(product_analyzer):
    """제품 분석 섹션을 표시합니다."""
    st.header("📦 제품 분석")
    
    # 2열 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            product_analyzer.create_category_pie_chart(),
            use_container_width=True,
            key="category_pie"
        )
    
    with col2:
        st.plotly_chart(
            product_analyzer.create_category_bar_chart(),
            use_container_width=True,
            key="category_bar"
        )
    
    # 제품 분류별 TOP 3
    st.subheader("제품 분류별 TOP 3 매출")
    top_products = product_analyzer.get_top_products_by_category(3)
    top_products_display = top_products.copy()
    top_products_display['매출액'] = top_products_display['매출액'].apply(lambda x: f"₩{x:,.0f}")
    top_products_display.columns = ['분류명', '순위', '제품명', '매출액', '거래건수', '판매수량']
    st.dataframe(top_products_display, use_container_width=True, hide_index=True)
    
    # 단가대별 분포
    st.plotly_chart(
        product_analyzer.create_price_distribution_chart(),
        use_container_width=True,
        key="price_distribution"
    )


def display_customer_section(customer_analyzer):
    """거래처 분석 섹션을 표시합니다."""
    st.header("🏢 거래처 분석")
    
    # TOP 10 거래처
    st.plotly_chart(
        customer_analyzer.create_top_customers_chart(10),
        use_container_width=True,
        key="top_customers"
    )
    
    # 거래 건수
    st.plotly_chart(
        customer_analyzer.create_customer_transaction_chart(10),
        use_container_width=True,
        key="customer_transactions"
    )
    
    # 거래처 상세 정보
    st.subheader("주요 거래처 상세 정보 (TOP 15)")
    customer_detail = customer_analyzer.get_customer_detail().head(15)
    customer_detail_display = customer_detail.copy()
    customer_detail_display['매출액'] = customer_detail_display['매출액'].apply(lambda x: f"₩{x:,.0f}")
    customer_detail_display['평균거래금액'] = customer_detail_display['평균거래금액'].apply(lambda x: f"₩{x:,.0f}")
    customer_detail_display['매출비중'] = customer_detail_display['매출비중'].apply(lambda x: f"{x}%")
    st.dataframe(customer_detail_display, use_container_width=True, hide_index=True)


def display_discount_section(discount_analyzer):
    """할인 분석 섹션을 표시합니다."""
    st.header("💰 할인 분석")
    
    # 2열 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            discount_analyzer.create_discount_application_chart(),
            use_container_width=True,
            key="discount_application"
        )
    
    with col2:
        discount_rate_chart = discount_analyzer.create_discount_rate_chart()
        if discount_rate_chart:
            st.plotly_chart(
                discount_rate_chart,
                use_container_width=True,
                key="discount_rate"
            )
        else:
            st.info("할인 데이터가 충분하지 않습니다.")
    
    # 제품 분류별 할인율
    st.plotly_chart(
        discount_analyzer.create_category_discount_chart(),
        use_container_width=True,
        key="category_discount"
    )


def main():
    """메인 함수"""
    
    # 헤더
    st.title("📊 판매 데이터 분석 대시보드")
    st.markdown(f"**{REPORT_CONFIG['title']}** - 생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}")
    st.markdown("---")
    
    # 사이드바 - 파일 업로드
    st.sidebar.header("📁 데이터 소스")
    
    # 파일 업로더
    uploaded_file = st.sidebar.file_uploader(
        "Excel 또는 CSV 파일 업로드 (선택사항)",
        type=['xlsx', 'xls', 'csv'],
        help="판매 데이터 파일을 업로드하세요. Excel (.xlsx, .xls) 또는 CSV (.csv) 형식을 지원합니다. 업로드하지 않으면 기본 파일(판매.xlsx)을 사용합니다."
    )
    
    # 시트명 입력 (Excel 파일인 경우에만 필요)
    sheet_name = "Sheet1"
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension in ['xlsx', 'xls']:
            sheet_name = st.sidebar.text_input(
                "시트명 (Excel 전용)",
                value="Sheet1",
                help="Excel 파일의 시트명을 입력하세요."
            )
        else:
            st.sidebar.info("ℹ️ CSV 파일은 시트명이 필요하지 않습니다.")
    
    st.sidebar.markdown("---")
    
    # 데이터 로드
    df = None
    data_info = None
    
    if uploaded_file is not None:
        # 업로드된 파일 사용
        st.sidebar.success(f"✅ 업로드된 파일: {uploaded_file.name}")
        with st.spinner('업로드된 파일을 로드하는 중...'):
            df, data_info = load_data_from_upload(uploaded_file, sheet_name)
    else:
        # 기본 파일 사용
        st.sidebar.info("ℹ️ 기본 파일(판매.xlsx) 사용 중")
        try:
            with st.spinner('기본 데이터를 로드하는 중...'):
                df, data_info = load_data_from_file('판매.xlsx', sheet_name)
        except Exception as e:
            st.error(f"❌ 기본 파일을 찾을 수 없습니다: {e}")
            st.info("📁 파일을 업로드하거나 '판매.xlsx' 파일을 프로젝트 폴더에 추가하세요.")
            st.stop()
    
    # 데이터 로드 실패 시 중단
    if df is None or data_info is None:
        st.stop()
    
    # 데이터 로드 성공 메시지
    st.sidebar.success(f"✅ 데이터 로드 완료: {len(df):,}건")
    
    # 사이드바 - 필터
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 필터 옵션")
    
    # 날짜 범위 선택
    st.sidebar.subheader("📅 기간 선택")
    
    min_date = df['날짜'].min().date()
    max_date = df['날짜'].max().date()
    
    date_range = st.sidebar.date_input(
        "날짜 범위",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )
    
    # 제품 분류 선택
    st.sidebar.subheader("📦 제품 분류")
    all_categories = sorted(df['분류명'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "제품 분류 선택 (전체 선택 시 비워두세요)",
        options=all_categories,
        default=[],
        key="categories"
    )
    
    # 거래처 선택
    st.sidebar.subheader("🏢 거래처")
    all_customers = sorted(df['거래처명'].unique().tolist())
    selected_customers = st.sidebar.multiselect(
        "거래처 선택 (전체 선택 시 비워두세요)",
        options=all_customers,
        default=[],
        key="customers"
    )
    
    # 필터 적용 버튼
    apply_filter = st.sidebar.button("✅ 필터 적용", type="primary", use_container_width=True)
    reset_filter = st.sidebar.button("🔄 필터 초기화", use_container_width=True)
    
    # 필터 초기화
    if reset_filter:
        st.rerun()
    
    # 데이터 필터링
    if apply_filter or (not selected_categories and not selected_customers):
        filtered_df = filter_data(df, date_range, selected_categories, selected_customers)
    else:
        filtered_df = df
    
    # 필터링된 데이터 정보 표시
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 데이터 요약")
    st.sidebar.metric("총 거래 건수", f"{len(filtered_df):,}건")
    st.sidebar.metric("거래처 수", f"{filtered_df['거래처명'].nunique():,}개")
    st.sidebar.metric("제품 종류", f"{filtered_df['제품명'].nunique():,}종")
    
    # 데이터 분석
    with st.spinner('데이터를 분석하는 중...'):
        # KPI 분석
        kpi_analyzer = KPIAnalyzer(filtered_df)
        kpis = kpi_analyzer.get_kpi_summary()
        
        # 시계열 분석
        timeseries_analyzer = TimeSeriesAnalyzer(filtered_df)
        
        # 제품 분석
        product_analyzer = ProductAnalyzer(filtered_df)
        
        # 거래처 분석
        customer_analyzer = CustomerAnalyzer(filtered_df)
        
        # 할인 분석
        discount_analyzer = DiscountAnalyzer(filtered_df)
    
    # 탭 생성
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 대시보드 개요",
        "📈 시계열 분석",
        "📦 제품 분석",
        "🏢 거래처 분석",
        "💰 할인 분석"
    ])
    
    with tab1:
        display_kpi_section(kpis)
    
    with tab2:
        display_timeseries_section(timeseries_analyzer)
    
    with tab3:
        display_product_section(product_analyzer)
    
    with tab4:
        display_customer_section(customer_analyzer)
    
    with tab5:
        display_discount_section(discount_analyzer)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>이 대시보드는 자동으로 생성되었습니다.</p>
            <p>문의사항이 있으시면 데이터 분석팀으로 연락 주시기 바랍니다.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        st.write("\n사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
        import traceback
        st.code(traceback.format_exc())
        sys.exit(1)

