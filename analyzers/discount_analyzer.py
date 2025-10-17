#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
할인 분석 모듈
할인율별 매출 분포, 할인 적용 현황 등을 분석합니다.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config import COLORS, CHART_COLORS, PLOTLY_LAYOUT, REPORT_CONFIG


class DiscountAnalyzer:
    """할인 분석 클래스"""
    
    def __init__(self, df):
        """
        Args:
            df: 판매 데이터프레임
        """
        self.df = df
    
    def get_discount_application(self):
        """할인 적용 거래 vs 정상가 거래를 비교합니다."""
        discount_app = self.df.groupby('할인적용').agg({
            '금액': 'sum',
            '판매ID': 'count'
        }).reset_index()
        discount_app.columns = ['할인적용', '매출액', '거래건수']
        discount_app['매출비중'] = (discount_app['매출액'] / discount_app['매출액'].sum() * 100).round(1)
        return discount_app
    
    def create_discount_application_chart(self):
        """할인 적용 거래 vs 정상가 거래 비교 차트를 생성합니다."""
        discount_app = self.get_discount_application()
        
        fig = go.Figure()
        
        # 도넛 차트
        fig.add_trace(go.Pie(
            labels=discount_app['할인적용'],
            values=discount_app['매출액'],
            hole=0.4,
            marker=dict(colors=[COLORS['primary_blue'], COLORS['light_blue']]),
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='%{label}<br>매출액: ₩%{value:,.0f}<br>비중: %{percent}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '할인 적용 vs 정상가 거래',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'height': 400,
            'annotations': [{
                'text': '매출액<br>기준',
                'x': 0.5, 'y': 0.5,
                'font': {'size': 14, 'color': COLORS['dark_gray']},
                'showarrow': False
            }]
        })
        
        fig.update_layout(**layout)
        return fig
    
    def get_discount_rate_distribution(self):
        """할인율별 매출 분포를 계산합니다."""
        # 할인율 구간 설정
        df_discount = self.df[self.df['Discount'] > 0].copy()
        
        if len(df_discount) == 0:
            return pd.DataFrame()
        
        bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
        labels = ['10% 미만', '10-20%', '20-30%', '30-40%', '40-50%', '50% 이상']
        
        df_discount['할인율구간'] = pd.cut(df_discount['Discount'], bins=bins, labels=labels)
        
        discount_dist = df_discount.groupby('할인율구간', observed=False).agg({
            '금액': 'sum',
            '판매ID': 'count',
            '할인액': 'sum'
        }).reset_index()
        discount_dist.columns = ['할인율구간', '매출액', '거래건수', '할인액']
        
        return discount_dist
    
    def create_discount_rate_chart(self):
        """할인율별 매출 분포 차트를 생성합니다."""
        discount_dist = self.get_discount_rate_distribution()
        
        if discount_dist.empty:
            return None
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=discount_dist['할인율구간'],
            y=discount_dist['매출액'],
            name='매출액',
            marker=dict(color=COLORS['primary_blue']),
            text=discount_dist['매출액'],
            texttemplate='₩%{text:,.0f}',
            textposition='outside',
            hovertemplate='%{x}<br>매출액: ₩%{y:,.0f}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '할인율별 매출 분포',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '할인율 구간',
                'showgrid': False,
                'color': COLORS['dark_gray']
            },
            'yaxis': {
                'title': '매출액 (원)',
                'showgrid': True,
                'gridcolor': COLORS['neutral_gray'],
                'color': COLORS['dark_gray']
            },
            'height': 400
        })
        
        fig.update_layout(**layout)
        return fig
    
    def get_category_discount(self):
        """제품 분류별 평균 할인율을 계산합니다."""
        category_discount = self.df.groupby('분류명').agg({
            'Discount': 'mean',
            '금액': 'sum',
            '할인액': 'sum'
        }).reset_index()
        category_discount.columns = ['분류명', '평균할인율', '매출액', '할인액']
        category_discount['평균할인율'] = (category_discount['평균할인율'] * 100).round(1)
        category_discount['할인비율'] = (category_discount['할인액'] / (category_discount['매출액'] + category_discount['할인액']) * 100).round(1)
        category_discount = category_discount.sort_values('평균할인율', ascending=False)
        return category_discount
    
    def create_category_discount_chart(self):
        """제품 분류별 평균 할인율 차트를 생성합니다."""
        category_discount = self.get_category_discount()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=category_discount['분류명'],
            x=category_discount['평균할인율'],
            orientation='h',
            marker=dict(color=COLORS['secondary_blue']),
            text=category_discount['평균할인율'],
            texttemplate='%{text:.1f}%',
            textposition='outside',
            hovertemplate='%{y}<br>평균 할인율: %{x:.1f}%<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '제품 분류별 평균 할인율',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '평균 할인율 (%)',
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
    
    def get_discount_summary(self):
        """할인 관련 요약 정보를 반환합니다."""
        total_discount = self.df['할인액'].sum() if '할인액' in self.df.columns else 0
        discount_count = len(self.df[self.df['Discount'] > 0])
        avg_discount_rate = self.df[self.df['Discount'] > 0]['Discount'].mean() * 100 if discount_count > 0 else 0
        
        return {
            'total_discount': total_discount,
            'discount_count': discount_count,
            'discount_ratio': round(discount_count / len(self.df) * 100, 1),
            'avg_discount_rate': round(avg_discount_rate, 1)
        }

