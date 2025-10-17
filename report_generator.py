#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보고서 생성 모듈
분석 결과를 HTML 보고서로 생성합니다.
"""

import pandas as pd
from datetime import datetime
from jinja2 import Template
from config import COLORS, REPORT_CONFIG


class ReportGenerator:
    """HTML 보고서 생성 클래스"""
    
    def __init__(self, data_info, kpis, analyzers):
        """
        Args:
            data_info: 데이터 정보 딕셔너리
            kpis: KPI 분석 결과
            analyzers: 분석기 객체들 (timeseries, product, customer, discount)
        """
        self.data_info = data_info
        self.kpis = kpis
        self.timeseries = analyzers['timeseries']
        self.product = analyzers['product']
        self.customer = analyzers['customer']
        self.discount = analyzers['discount']
        self.report_html = ""
    
    def generate_html(self):
        """전체 HTML 보고서를 생성합니다."""
        html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Malgun Gothic', 'Arial', sans-serif;
            background-color: {{ colors.white }};
            color: {{ colors.dark_gray }};
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, {{ colors.primary_blue }} 0%, {{ colors.secondary_blue }} 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .header .subtitle {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .section {
            background: {{ colors.white }};
            border: 1px solid {{ colors.border }};
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: {{ colors.primary_blue }};
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid {{ colors.primary_blue }};
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .kpi-card {
            background: {{ colors.light_gray }};
            border-left: 4px solid {{ colors.primary_blue }};
            padding: 20px;
            border-radius: 8px;
            transition: transform 0.2s;
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .kpi-label {
            font-size: 14px;
            color: {{ colors.dark_gray }};
            margin-bottom: 8px;
        }
        
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
            color: {{ colors.primary_blue }};
        }
        
        .chart-container {
            margin: 20px 0;
            background: {{ colors.white }};
            padding: 15px;
            border-radius: 8px;
        }
        
        .grid-2col {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }
        
        table thead {
            background-color: {{ colors.primary_blue }};
            color: white;
        }
        
        table th {
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        
        table td {
            padding: 10px 12px;
            border-bottom: 1px solid {{ colors.neutral_gray }};
        }
        
        table tbody tr:nth-child(even) {
            background-color: {{ colors.light_gray }};
        }
        
        table tbody tr:hover {
            background-color: {{ colors.neutral_gray }};
        }
        
        table td.number {
            text-align: right;
        }
        
        table td.text-center {
            text-align: center;
        }
        
        table td.category-name {
            font-weight: bold;
        }
        
        table tr.group-header-row {
            background-color: #F0F7FC;
        }
        
        table tr.group-header-row:hover {
            background-color: #E3F2FD;
        }
        
        table tr.group-separator {
            height: 2px;
        }
        
        table tr.group-separator td {
            padding: 0;
            border: none;
        }
        
        .footer {
            text-align: center;
            padding: 30px 20px;
            color: {{ colors.dark_gray }};
            font-size: 14px;
            border-top: 1px solid {{ colors.border }};
            margin-top: 40px;
        }
        
        .data-info {
            background: {{ colors.light_gray }};
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .data-info-item {
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 10px;
        }
        
        .data-info-label {
            font-weight: bold;
            color: {{ colors.dark_gray }};
        }
        
        @media print {
            .section {
                page-break-inside: avoid;
            }
        }
        
        @media (max-width: 768px) {
            .grid-2col {
                grid-template-columns: 1fr;
            }
            
            .kpi-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <div class="header">
            <h1>{{ report_title }}</h1>
            <div class="subtitle">{{ data_period }}</div>
            <div class="subtitle">보고서 생성일: {{ generated_date }}</div>
        </div>
        
        <!-- 데이터 개요 -->
        <div class="data-info">
            <div class="data-info-item">
                <span class="data-info-label">데이터 기간:</span> {{ data_start }} ~ {{ data_end }}
            </div>
            <div class="data-info-item">
                <span class="data-info-label">총 거래 건수:</span> {{ total_records }}건
            </div>
            <div class="data-info-item">
                <span class="data-info-label">거래처 수:</span> {{ customer_count }}개
            </div>
            <div class="data-info-item">
                <span class="data-info-label">제품 종류:</span> {{ product_count }}종
            </div>
        </div>
        
        <!-- 1. 대시보드 개요 (KPI) -->
        <div class="section">
            <h2 class="section-title">📊 1. 대시보드 개요</h2>
            <div class="kpi-grid">
                {% for kpi in main_kpis %}
                <div class="kpi-card">
                    <div class="kpi-label">{{ kpi.label }}</div>
                    <div class="kpi-value">{{ kpi.formatted }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="kpi-grid">
                {% for kpi in sub_kpis %}
                <div class="kpi-card">
                    <div class="kpi-label">{{ kpi.label }}</div>
                    <div class="kpi-value">{{ kpi.formatted }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <!-- 2. 시계열 분석 -->
        <div class="section">
            <h2 class="section-title">📈 2. 시계열 분석</h2>
            <div class="chart-container">
                <div id="monthly-sales-chart"></div>
            </div>
            <div class="grid-2col">
                <div class="chart-container">
                    <div id="monthly-transactions-chart"></div>
                </div>
                <div class="chart-container">
                    <div id="quarterly-sales-chart"></div>
                </div>
            </div>
            <div class="chart-container">
                <div id="weekday-chart"></div>
            </div>
        </div>
        
        <!-- 3. 제품 분석 -->
        <div class="section">
            <h2 class="section-title">📦 3. 제품 분석</h2>
            <div class="grid-2col">
                <div class="chart-container">
                    <div id="category-pie-chart"></div>
                </div>
                <div class="chart-container">
                    <div id="category-bar-chart"></div>
                </div>
            </div>
            <h3 style="margin-top: 30px; margin-bottom: 15px; color: {{ colors.primary_blue }};">제품 분류별 TOP 3 매출</h3>
            {{ top_products_by_category_table }}
            <div class="chart-container">
                <div id="price-distribution-chart"></div>
            </div>
        </div>
        
        <!-- 4. 거래처 분석 -->
        <div class="section">
            <h2 class="section-title">🏢 4. 거래처 분석</h2>
            <div class="chart-container">
                <div id="top-customers-chart"></div>
            </div>
            <div class="chart-container">
                <div id="customer-transactions-chart"></div>
            </div>
            <h3 style="margin-top: 30px; margin-bottom: 15px; color: {{ colors.primary_blue }};">주요 거래처 상세 정보</h3>
            {{ customer_detail_table }}
        </div>
        
        <!-- 5. 할인 분석 -->
        <div class="section">
            <h2 class="section-title">💰 5. 할인 분석</h2>
            <div class="grid-2col">
                <div class="chart-container">
                    <div id="discount-application-chart"></div>
                </div>
                {% if discount_rate_chart %}
                <div class="chart-container">
                    <div id="discount-rate-chart"></div>
                </div>
                {% endif %}
            </div>
            <div class="chart-container">
                <div id="category-discount-chart"></div>
            </div>
        </div>
        
        <!-- 푸터 -->
        <div class="footer">
            <p>이 보고서는 자동으로 생성되었습니다.</p>
            <p>문의사항이 있으시면 데이터 분석팀으로 연락 주시기 바랍니다.</p>
        </div>
    </div>
    
    <!-- 차트 렌더링 스크립트 -->
    <script>
        {{ chart_scripts }}
    </script>
</body>
</html>
        """
        
        # 템플릿 데이터 준비
        template_data = self._prepare_template_data()
        
        # Jinja2 템플릿 렌더링
        template = Template(html_template)
        self.report_html = template.render(**template_data)
        
        return self.report_html
    
    def _prepare_template_data(self):
        """템플릿에 전달할 데이터를 준비합니다."""
        # KPI 요약
        kpi_summary = self.kpis
        
        # 제품 분류별 TOP 3 테이블
        top_products_by_category = self.product.get_top_products_by_category(3)
        top_products_formatted = top_products_by_category.copy()
        top_products_formatted['매출액'] = top_products_formatted['매출액'].apply(lambda x: f"₩{x:,.0f}")
        top_products_formatted.columns = ['분류명', '순위', '제품명', '매출액', '거래건수', '판매수량']
        top_products_html = self._df_to_html_table_grouped(top_products_formatted, '분류명')
        
        # 거래처 상세 정보 테이블
        customer_detail = self.customer.get_customer_detail().head(15)
        customer_detail_formatted = customer_detail.copy()
        customer_detail_formatted['매출액'] = customer_detail_formatted['매출액'].apply(lambda x: f"₩{x:,.0f}")
        customer_detail_formatted['평균거래금액'] = customer_detail_formatted['평균거래금액'].apply(lambda x: f"₩{x:,.0f}")
        customer_detail_formatted['매출비중'] = customer_detail_formatted['매출비중'].apply(lambda x: f"{x}%")
        customer_detail_html = self._df_to_html_table(customer_detail_formatted)
        
        # 차트 스크립트 생성
        chart_scripts = self._generate_chart_scripts()
        
        # 데이터 기간 포맷팅
        data_start = self.data_info['데이터_시작일'].strftime('%Y년 %m월 %d일')
        data_end = self.data_info['데이터_종료일'].strftime('%Y년 %m월 %d일')
        data_period = f"{data_start} ~ {data_end}"
        
        return {
            'report_title': REPORT_CONFIG['title'],
            'generated_date': datetime.now().strftime('%Y년 %m월 %d일 %H:%M'),
            'data_period': data_period,
            'data_start': data_start,
            'data_end': data_end,
            'total_records': f"{self.data_info['총_거래건수']:,}",
            'customer_count': self.data_info['거래처_수'],
            'product_count': self.data_info['제품_수'],
            'colors': COLORS,
            'main_kpis': kpi_summary['main_kpis'],
            'sub_kpis': kpi_summary['sub_kpis'],
            'top_products_by_category_table': top_products_html,
            'customer_detail_table': customer_detail_html,
            'discount_rate_chart': self.discount.get_discount_rate_distribution().empty == False,
            'chart_scripts': chart_scripts
        }
    
    def _df_to_html_table(self, df):
        """데이터프레임을 HTML 테이블로 변환합니다."""
        html = "<table>\n<thead>\n<tr>\n"
        for col in df.columns:
            html += f"<th>{col}</th>\n"
        html += "</tr>\n</thead>\n<tbody>\n"
        
        for _, row in df.iterrows():
            html += "<tr>\n"
            for val in row:
                # 모든 컬럼을 왼쪽 정렬
                html += f"<td>{val}</td>\n"
            html += "</tr>\n"
        
        html += "</tbody>\n</table>"
        return html
    
    def _df_to_html_table_grouped(self, df, group_column):
        """데이터프레임을 그룹별로 구분된 HTML 테이블로 변환합니다."""
        html = "<table>\n<thead>\n<tr>\n"
        for col in df.columns:
            html += f"<th>{col}</th>\n"
        html += "</tr>\n</thead>\n<tbody>\n"
        
        current_group = None
        for idx, row in df.iterrows():
            group_value = row[group_column]
            
            # 그룹이 바뀔 때 구분선과 배경색 변경
            if current_group != group_value:
                if current_group is not None:
                    # 그룹 구분선 추가
                    html += "<tr class='group-separator'><td colspan='{}' style='height: 2px; background-color: {}'></td></tr>\n".format(
                        len(df.columns), COLORS['primary_blue']
                    )
                current_group = group_value
                row_class = 'group-header-row'
            else:
                row_class = 'group-row'
            
            html += f"<tr class='{row_class}'>\n"
            for i, val in enumerate(row):
                # 모든 컬럼을 왼쪽 정렬하되, 분류명은 색상과 굵기 유지
                if i == 0:  # 분류명
                    css_class = 'category-name'
                    style = f"font-weight: bold; color: {COLORS['primary_blue']};"
                else:
                    css_class = ''
                    style = ""
                
                html += f"<td class='{css_class}' style='{style}'>{val}</td>\n"
            html += "</tr>\n"
        
        html += "</tbody>\n</table>"
        return html
    
    def _generate_chart_scripts(self):
        """모든 차트의 Plotly 스크립트를 생성합니다."""
        scripts = []
        
        # 시계열 차트
        scripts.append(self._fig_to_script(self.timeseries.create_monthly_sales_chart(), 'monthly-sales-chart'))
        scripts.append(self._fig_to_script(self.timeseries.create_monthly_transactions_chart(), 'monthly-transactions-chart'))
        scripts.append(self._fig_to_script(self.timeseries.create_quarterly_sales_chart(), 'quarterly-sales-chart'))
        scripts.append(self._fig_to_script(self.timeseries.create_weekday_chart(), 'weekday-chart'))
        
        # 제품 차트
        scripts.append(self._fig_to_script(self.product.create_category_pie_chart(), 'category-pie-chart'))
        scripts.append(self._fig_to_script(self.product.create_category_bar_chart(), 'category-bar-chart'))
        scripts.append(self._fig_to_script(self.product.create_price_distribution_chart(), 'price-distribution-chart'))
        
        # 거래처 차트
        scripts.append(self._fig_to_script(self.customer.create_top_customers_chart(), 'top-customers-chart'))
        scripts.append(self._fig_to_script(self.customer.create_customer_transaction_chart(), 'customer-transactions-chart'))
        
        # 할인 차트
        scripts.append(self._fig_to_script(self.discount.create_discount_application_chart(), 'discount-application-chart'))
        
        discount_rate_chart = self.discount.create_discount_rate_chart()
        if discount_rate_chart:
            scripts.append(self._fig_to_script(discount_rate_chart, 'discount-rate-chart'))
        
        scripts.append(self._fig_to_script(self.discount.create_category_discount_chart(), 'category-discount-chart'))
        
        return '\n'.join(scripts)
    
    def _fig_to_script(self, fig, div_id):
        """Plotly Figure를 JavaScript 스크립트로 변환합니다."""
        if fig is None:
            return ""
        
        import json
        import numpy as np
        
        def convert_to_serializable(obj):
            """Plotly 객체를 JSON 직렬화 가능한 형태로 변환"""
            if obj is None:
                return None
            elif isinstance(obj, (int, float, str, bool)):
                return obj
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_to_serializable(value) for key, value in obj.items()}
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif hasattr(obj, 'tolist'):  # pandas Series 등
                return obj.tolist()
            elif hasattr(obj, 'to_plotly_json'):  # Plotly 객체
                return obj.to_plotly_json()
            elif hasattr(obj, '__dict__'):  # 다른 객체
                return {key: convert_to_serializable(value) for key, value in obj.__dict__.items() if not key.startswith('_')}
            else:
                return str(obj)
        
        # Figure의 데이터를 JSON 직렬화 가능한 형태로 변환
        data = []
        for trace in fig.data:
            trace_json = trace.to_plotly_json()
            # numpy 배열을 리스트로 변환
            for key, value in trace_json.items():
                if isinstance(value, np.ndarray):
                    trace_json[key] = value.tolist()
                elif hasattr(value, 'tolist'):
                    trace_json[key] = value.tolist()
            data.append(trace_json)
        
        # Layout도 딕셔너리로 변환
        layout = fig.layout.to_plotly_json()
        
        config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'locale': 'ko'
        }
        
        # JSON 문자열로 변환
        data_json = json.dumps(data, ensure_ascii=False)
        layout_json = json.dumps(layout, ensure_ascii=False)
        config_json = json.dumps(config)
        
        return f"Plotly.newPlot('{div_id}', {data_json}, {layout_json}, {config_json});"
    
    def save_report(self, output_path):
        """보고서를 HTML 파일로 저장합니다."""
        if not self.report_html:
            self.generate_html()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.report_html)
        
        print(f"✓ 보고서 저장 완료: {output_path}")

