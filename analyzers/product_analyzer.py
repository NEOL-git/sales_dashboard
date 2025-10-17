#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
제품 분석 모듈
제품별, 제품 분류별, 색상별 판매 현황을 분석합니다.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS, CHART_COLORS, PLOTLY_LAYOUT, REPORT_CONFIG


class ProductAnalyzer:
    """제품 분석 클래스"""
    
    def __init__(self, df):
        """
        Args:
            df: 판매 데이터프레임
        """
        self.df = df
    
    def get_category_sales(self):
        """제품 분류별 매출을 계산합니다."""
        category = self.df.groupby('분류명').agg({
            '금액': 'sum',
            '판매ID': 'count',
            '수량': 'sum'
        }).reset_index()
        category.columns = ['분류명', '매출액', '거래건수', '판매수량']
        category = category.sort_values('매출액', ascending=False)
        category['매출비중'] = (category['매출액'] / category['매출액'].sum() * 100).round(1)
        return category
    
    def create_category_pie_chart(self):
        """제품 분류별 매출 비중 파이 차트를 생성합니다."""
        category = self.get_category_sales()
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=category['분류명'],
            values=category['매출액'],
            marker=dict(colors=CHART_COLORS),
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='%{label}<br>매출액: ₩%{value:,.0f}<br>비중: %{percent}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '제품 분류별 매출 비중',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'height': 450,
            'showlegend': True,
            'legend': {
                'orientation': 'v',
                'yanchor': 'middle',
                'y': 0.5,
                'xanchor': 'left',
                'x': 1.02
            }
        })
        
        fig.update_layout(**layout)
        return fig
    
    def create_category_bar_chart(self):
        """제품 분류별 매출액 순위 바 차트를 생성합니다."""
        category = self.get_category_sales()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=category['분류명'],
            x=category['매출액'],
            orientation='h',
            marker=dict(color=COLORS['primary_blue']),
            text=category['매출액'],
            texttemplate='₩%{text:,.0f}',
            textposition='outside',
            hovertemplate='%{y}<br>매출액: ₩%{x:,.0f}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '제품 분류별 매출액 순위',
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
                'color': COLORS['dark_gray'],
                'autorange': 'reversed'
            },
            'height': 400
        })
        
        fig.update_layout(**layout)
        return fig
    
    def get_top_products(self, top_n=10):
        """제품별 TOP N 매출을 계산합니다."""
        products = self.df.groupby(['제품코드', '제품명', '분류명']).agg({
            '금액': 'sum',
            '판매ID': 'count',
            '수량': 'sum'
        }).reset_index()
        products.columns = ['제품코드', '제품명', '분류명', '매출액', '거래건수', '판매수량']
        products = products.sort_values('매출액', ascending=False).head(top_n)
        products['순위'] = range(1, len(products) + 1)
        return products[['순위', '제품명', '분류명', '매출액', '거래건수', '판매수량']]
    
    def get_top_products_by_category(self, top_n=3):
        """제품 분류별 TOP N 매출 제품을 계산합니다. (테이블 형식)"""
        products = self.df.groupby(['분류명', '제품코드', '제품명']).agg({
            '금액': 'sum',
            '판매ID': 'count',
            '수량': 'sum'
        }).reset_index()
        products.columns = ['분류명', '제품코드', '제품명', '매출액', '거래건수', '판매수량']
        
        # 분류명을 매출액 순으로 정렬
        category_order = self.get_category_sales()['분류명'].tolist()
        
        # 각 분류별로 상위 N개 제품 선택
        top_products_list = []
        for category in category_order:
            category_data = products[products['분류명'] == category].nlargest(top_n, '매출액').copy()
            # 분류 내 순위 추가
            category_data['분류내순위'] = range(1, len(category_data) + 1)
            top_products_list.append(category_data)
        
        top_products = pd.concat(top_products_list, ignore_index=True)
        
        # 테이블 형식에 맞게 컬럼 재정렬
        return top_products[['분류명', '분류내순위', '제품명', '매출액', '거래건수', '판매수량']]
    
    def get_price_distribution(self):
        """단가대별 제품 분포를 계산합니다."""
        # 단가대 구간 설정
        bins = [0, 50000, 100000, 200000, 500000, 1000000, float('inf')]
        labels = ['5만원 미만', '5-10만원', '10-20만원', '20-50만원', '50-100만원', '100만원 이상']
        
        df_temp = self.df.copy()
        df_temp['단가대'] = pd.cut(df_temp['단가'], bins=bins, labels=labels)
        
        price_dist = df_temp.groupby('단가대', observed=False).agg({
            '금액': 'sum',
            '판매ID': 'count'
        }).reset_index()
        price_dist.columns = ['단가대', '매출액', '거래건수']
        
        return price_dist
    
    def create_price_distribution_chart(self):
        """단가대별 제품 분포 차트를 생성합니다."""
        price_dist = self.get_price_distribution()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=price_dist['단가대'],
            y=price_dist['거래건수'],
            marker=dict(color=COLORS['light_blue']),
            text=price_dist['거래건수'],
            texttemplate='%{text:,.0f}건',
            textposition='outside',
            hovertemplate='%{x}<br>거래건수: %{y:,.0f}건<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '단가대별 제품 분포',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '단가대',
                'showgrid': False,
                'color': COLORS['dark_gray']
            },
            'yaxis': {
                'title': '거래 건수',
                'showgrid': True,
                'gridcolor': COLORS['neutral_gray'],
                'color': COLORS['dark_gray']
            },
            'height': 400
        })
        
        fig.update_layout(**layout)
        return fig

