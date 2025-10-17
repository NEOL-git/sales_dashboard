#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시계열 분석 모듈
월별, 분기별, 요일별 판매 추이를 분석합니다.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS, CHART_COLORS, PLOTLY_LAYOUT, REPORT_CONFIG


class TimeSeriesAnalyzer:
    """시계열 분석 클래스"""
    
    def __init__(self, df):
        """
        Args:
            df: 판매 데이터프레임
        """
        self.df = df
    
    def get_monthly_sales(self):
        """월별 매출액을 계산합니다."""
        # 년월별로 그룹화하여 매출액 합계와 거래건수 계산
        monthly = self.df.groupby(['년', '월'], as_index=False).agg({
            '금액': 'sum',
            '수량': 'sum'
        })
        monthly.columns = ['년', '월', '매출액', '거래건수']
        
        # 년월 컬럼 생성 (정렬 및 표시용)
        monthly['년월'] = monthly['년'].astype(str) + '-' + monthly['월'].astype(str).str.zfill(2)
        
        # 년, 월 순으로 정렬
        monthly = monthly.sort_values(['년', '월'])
        
        return monthly
    
    def create_monthly_sales_chart(self):
        """월별 매출 추이 차트를 생성합니다."""
        monthly = self.get_monthly_sales()
        
        fig = go.Figure()
        
        # 세로형 막대 그래프 (월별 매출액 합계)
        fig.add_trace(go.Bar(
            x=monthly['년월'],
            y=monthly['매출액'],
            name='월별 매출액',
            marker=dict(color=COLORS['light_blue']),
            text=monthly['매출액'],
            texttemplate='₩%{text:,.0f}',
            textposition='outside',
            textfont=dict(size=10),
            hovertemplate='%{x}<br>매출액 합계: ₩%{y:,.0f}<extra></extra>',
            orientation='v'  # 세로형 명시
        ))
        
        # 추이선 (막대 상단 연결)
        fig.add_trace(go.Scatter(
            x=monthly['년월'],
            y=monthly['매출액'],
            mode='lines+markers',
            name='추이선',
            line=dict(color=COLORS['primary_blue'], width=3),
            marker=dict(size=8, color=COLORS['primary_blue']),
            hovertemplate='%{x}<br>매출액: ₩%{y:,.0f}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '월별 매출 추이',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '기간 (년-월)',
                'showgrid': False,
                'color': COLORS['dark_gray'],
                'tickangle': -45  # X축 라벨 회전
            },
            'yaxis': {
                'title': '매출액 합계 (원)',
                'showgrid': True,
                'gridcolor': COLORS['neutral_gray'],
                'color': COLORS['dark_gray']
            },
            'height': 450,
            'showlegend': True,
            'barmode': 'group'  # 막대 그룹 모드
        })
        
        fig.update_layout(**layout)
        return fig
    
    def get_quarterly_sales(self):
        """분기별 매출을 계산합니다."""
        quarterly = self.df.groupby(['년', '분기']).agg({
            '금액': 'sum',
            '판매ID': 'count'
        }).reset_index()
        quarterly['분기명'] = quarterly['년'].astype(str) + 'Q' + quarterly['분기'].astype(str)
        quarterly = quarterly.sort_values(['년', '분기'])
        return quarterly
    
    def create_quarterly_sales_chart(self):
        """분기별 매출 비교 차트를 생성합니다."""
        quarterly = self.get_quarterly_sales()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=quarterly['분기명'],
            y=quarterly['금액'],
            name='매출액',
            marker=dict(color=COLORS['primary_blue']),
            text=quarterly['금액'],
            texttemplate='₩%{text:,.0f}',
            textposition='outside',
            hovertemplate='%{x}<br>매출액: ₩%{y:,.0f}<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '분기별 매출 비교',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '분기',
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
    
    def get_weekday_pattern(self):
        """요일별 판매 패턴을 분석합니다."""
        요일_순서 = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday = self.df.groupby('요일명').agg({
            '금액': 'sum',
            '판매ID': 'count'
        }).reset_index()
        weekday.columns = ['요일', '매출액', '거래건수']
        
        # 요일 순서 정렬
        weekday['요일'] = pd.Categorical(weekday['요일'], categories=요일_순서, ordered=True)
        weekday = weekday.sort_values('요일')
        
        return weekday
    
    def create_weekday_chart(self):
        """요일별 판매 패턴 차트를 생성합니다."""
        weekday = self.get_weekday_pattern()
        
        fig = go.Figure()
        
        # customdata에 거래건수 추가
        fig.add_trace(go.Bar(
            x=weekday['요일'],
            y=weekday['매출액'],
            name='매출액',
            marker=dict(color=COLORS['secondary_blue']),
            text=weekday['매출액'],
            texttemplate='₩%{text:,.0f}',
            textposition='outside',
            customdata=weekday['거래건수'],
            hovertemplate='%{x}<br>매출액: ₩%{y:,.0f}<br>거래건수: %{customdata:,}건<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '요일별 판매 패턴',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '요일',
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
    
    def get_monthly_transactions(self):
        """월별 거래 건수를 계산합니다."""
        monthly = self.get_monthly_sales()
        return monthly[['년월', '거래건수']]
    
    def create_monthly_transactions_chart(self):
        """월별 거래 건수 추이 차트를 생성합니다."""
        monthly = self.get_monthly_sales()
        
        fig = go.Figure()
        
        # 세로형 막대 그래프 (월별 거래건수 합계)
        fig.add_trace(go.Bar(
            x=monthly['년월'],
            y=monthly['거래건수'],
            name='월별 거래건수',
            marker=dict(color=COLORS['light_blue']),
            text=monthly['거래건수'],
            texttemplate='%{text:,.0f}건',
            textposition='outside',
            textfont=dict(size=10),
            hovertemplate='%{x}<br>거래건수 합계: %{y:,.0f}건<extra></extra>',
            orientation='v'  # 세로형 명시
        ))
        
        # 추이선 (막대 상단 연결)
        fig.add_trace(go.Scatter(
            x=monthly['년월'],
            y=monthly['거래건수'],
            mode='lines+markers',
            name='추이선',
            line=dict(color=COLORS['primary_blue'], width=3),
            marker=dict(size=8, color=COLORS['primary_blue']),
            hovertemplate='%{x}<br>거래건수: %{y:,.0f}건<extra></extra>'
        ))
        
        # 레이아웃 설정
        layout = PLOTLY_LAYOUT.copy()
        layout.update({
            'title': {
                'text': '월별 거래 건수 추이',
                'font': {'size': 16, 'weight': 'bold', 'color': COLORS['dark_gray']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'title': '기간 (년-월)',
                'showgrid': False,
                'color': COLORS['dark_gray'],
                'tickangle': -45  # X축 라벨 회전
            },
            'yaxis': {
                'title': '거래건수 합계 (건)',
                'showgrid': True,
                'gridcolor': COLORS['neutral_gray'],
                'color': COLORS['dark_gray']
            },
            'height': 450,
            'showlegend': True,
            'barmode': 'group'  # 막대 그룹 모드
        })
        
        fig.update_layout(**layout)
        return fig

