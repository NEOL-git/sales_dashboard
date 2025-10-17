#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
거래처 분석 모듈
거래처별 매출, 거래 건수 등을 분석합니다.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config import COLORS, PLOTLY_LAYOUT, REPORT_CONFIG


class CustomerAnalyzer:
    """거래처 분석 클래스"""
    
    def __init__(self, df):
        """
        Args:
            df: 판매 데이터프레임
        """
        self.df = df
    
    def get_customer_sales(self):
        """거래처별 매출을 계산합니다."""
        customer = self.df.groupby('거래처명').agg({
            '금액': 'sum',
            '판매ID': 'count',
            '수량': 'sum'
        }).reset_index()
        customer.columns = ['거래처명', '매출액', '거래건수', '판매수량']
        customer = customer.sort_values('매출액', ascending=False)
        customer['매출비중'] = (customer['매출액'] / customer['매출액'].sum() * 100).round(1)
        return customer
    
    def get_top_customers(self, top_n=10):
        """거래처별 TOP N 매출을 계산합니다."""
        customer = self.get_customer_sales()
        top_customers = customer.head(top_n).copy()
        top_customers['순위'] = range(1, len(top_customers) + 1)
        return top_customers[['순위', '거래처명', '매출액', '거래건수', '판매수량', '매출비중']]
    
    def create_top_customers_chart(self, top_n=10):
        """거래처별 매출액 TOP N 바 차트를 생성합니다."""
        top_customers = self.get_top_customers(top_n)
        
        # 매출액 구간별 파스텔톤 색상 정의
        def get_color_by_sales(sales):
            """매출액 구간에 따라 파스텔톤 색상 반환"""
            if sales >= 250_000_000:  # 250M 이상
                return '#6CB4EE'  # 파스텔 블루
            elif sales >= 200_000_000:  # 200M ~ 250M
                return '#A8E6CF'  # 파스텔 그린
            elif sales >= 150_000_000:  # 150M ~ 200M
                return '#FFD3B6'  # 파스텔 오렌지
            else:  # 150M 미만
                return '#FFAAA5'  # 파스텔 핑크
        
        # 각 거래처의 매출액에 따라 색상 지정
        colors = [get_color_by_sales(sales) for sales in top_customers['매출액'][::-1]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_customers['거래처명'][::-1],  # 역순으로 표시
            x=top_customers['매출액'][::-1],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='white', width=1.5)  # 막대 사이 구분선
            ),
            text=top_customers['매출액'][::-1],
            texttemplate='₩%{text:,.0f}',
            textposition='outside',
            textfont=dict(size=10),
            hovertemplate='%{y}<br>매출액: ₩%{x:,.0f}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': f'거래처별 매출액 TOP {top_n}',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '매출액 (원)',
                'showgrid': True,
                'gridcolor': COLORS['neutral_gray'],
                'color': COLORS['dark_gray']
            },
            'yaxis': {
                'title': '',
                'showgrid': False,
                'color': COLORS['dark_gray']
            },
            'height': 500,
            'annotations': [
                # 그래프 내부 오른쪽 하단에 색상 구간 설명 추가
                dict(
                    x=0.98, y=0.02,
                    xref='paper', yref='paper',
                    text='<b>매출액 구간</b><br>' +
                         '<span style="color:#6CB4EE">●</span> 250M 이상<br>' +
                         '<span style="color:#A8E6CF">●</span> 200~250M<br>' +
                         '<span style="color:#FFD3B6">●</span> 150~200M<br>' +
                         '<span style="color:#FFAAA5">●</span> 150M 미만',
                    showarrow=False,
                    font=dict(size=10, color=COLORS['dark_gray']),
                    align='left',
                    xanchor='right',
                    yanchor='bottom',
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor=COLORS['neutral_gray'],
                    borderwidth=1,
                    borderpad=8
                )
            ]
        })
        
        fig.update_layout(**layout)
        return fig
    
    def get_customer_transaction_count(self):
        """거래처별 거래 건수를 계산합니다."""
        customer = self.get_customer_sales()
        return customer[['거래처명', '거래건수']].sort_values('거래건수', ascending=False)
    
    def create_customer_transaction_chart(self, top_n=10):
        """거래처별 거래 건수 차트를 생성합니다."""
        customer_trans = self.get_customer_transaction_count().head(top_n)
        
        # 거래건수에 따라 무채색 그라데이션 적용 (많을수록 진한 회색)
        max_count = customer_trans['거래건수'].max()
        min_count = customer_trans['거래건수'].min()
        
        def get_gray_color(count):
            """거래건수에 따라 회색 농도 반환"""
            # 정규화: 0(연한 회색) ~ 1(진한 회색)
            if max_count == min_count:
                normalized = 0.5
            else:
                normalized = (count - min_count) / (max_count - min_count)
            
            # 회색 범위: #D3D3D3 (연한 회색) ~ #696969 (진한 회색)
            # RGB 값 계산
            light_gray = 211  # #D3D3D3
            dark_gray = 105   # #696969
            gray_value = int(light_gray - (light_gray - dark_gray) * normalized)
            
            return f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
        
        colors = [get_gray_color(count) for count in customer_trans['거래건수']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=customer_trans['거래처명'],
            y=customer_trans['거래건수'],
            marker=dict(
                color=colors,
                line=dict(color='white', width=1)
            ),
            text=customer_trans['거래건수'],
            texttemplate='%{text:,.0f}건',
            textposition='outside',
            textfont=dict(size=10),
            hovertemplate='%{x}<br>거래건수: %{y:,.0f}건<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        
        # Y축 범위 계산 (텍스트가 잘리지 않도록 여유 공간 확보)
        y_max = max_count * 1.15  # 최대값의 115%로 설정하여 텍스트 표시 공간 확보
        
        layout.update({
            'title': {
                'text': f'거래처별 거래 건수 TOP {top_n}',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '거래처',
                'showgrid': False,
                'color': COLORS['dark_gray'],
                'tickangle': -45
            },
            'yaxis': {
                'title': '거래 건수',
                'showgrid': True,
                'gridcolor': COLORS['neutral_gray'],
                'color': COLORS['dark_gray'],
                'range': [0, y_max]  # Y축 범위 명시적 설정
            },
            'height': 400,
            'margin': {'b': 120}
        })
        
        fig.update_layout(**layout)
        return fig
    
    def get_customer_detail(self):
        """주요 거래처 상세 정보를 반환합니다."""
        customer = self.get_customer_sales()
        
        # 평균 거래 금액 추가
        customer['평균거래금액'] = (customer['매출액'] / customer['거래건수']).round(0)
        
        # 매출액 순으로 정렬 (내림차순)
        customer = customer.sort_values('매출액', ascending=False)
        
        # 순위 컬럼 추가
        customer['순위'] = range(1, len(customer) + 1)
        
        return customer[['순위', '거래처명', '매출액', '거래건수', '평균거래금액', '매출비중']]
    
    def get_customer_concentration(self):
        """거래처 집중도를 분석합니다."""
        customer = self.get_customer_sales()
        total_sales = customer['매출액'].sum()
        
        # 상위 거래처의 매출 비중 계산
        top_5_ratio = customer.head(5)['매출액'].sum() / total_sales * 100
        top_10_ratio = customer.head(10)['매출액'].sum() / total_sales * 100
        top_20_ratio = customer.head(20)['매출액'].sum() / total_sales * 100
        
        return {
            'top_5': round(top_5_ratio, 1),
            'top_10': round(top_10_ratio, 1),
            'top_20': round(top_20_ratio, 1),
            'total_customers': len(customer)
        }

