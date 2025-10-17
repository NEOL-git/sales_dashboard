#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보고서 디자인 설정
디자인 가이드의 색상 팔레트와 폰트 설정을 정의합니다.
"""

# 색상 팔레트 (디자인 가이드 기준)
COLORS = {
    'primary_blue': '#0A5CA4',      # 강조요소, 선택된 막대/라인
    'secondary_blue': '#5DA8D4',    # 누적 영역, 보조 요소
    'light_blue': '#A9CCE3',        # 도넛/파이 차트의 다른 구간
    'neutral_gray': '#D9D9D9',      # 배경 막대, 표 셰이딩
    'dark_gray': '#333333',         # 축, 본문 텍스트
    'light_gray': '#F5F5F5',        # 카드 배경, 표 행 배경
    'white': '#FFFFFF',             # 전체 배경, 기본 캔버스
    'border': '#E0E0E0',            # 카드 테두리
}

# 차트용 색상 팔레트 (여러 항목 표시용)
CHART_COLORS = [
    '#0A5CA4',  # Primary Blue
    '#5DA8D4',  # Secondary Blue
    '#A9CCE3',  # Light Blue
    '#7CB9E8',  # Medium Blue
    '#4A90E2',  # Sky Blue
    '#6C8EBF',  # Muted Blue
    '#8BB8D8',  # Powder Blue
    '#5B9BD5',  # Steel Blue
]

# 폰트 설정
FONTS = {
    'title': {
        'family': 'Arial, Segoe UI, Malgun Gothic, sans-serif',
        'size': 22,
        'weight': 'bold',
        'color': COLORS['dark_gray']
    },
    'subtitle': {
        'family': 'Arial, Segoe UI, Malgun Gothic, sans-serif',
        'size': 16,
        'weight': 'bold',
        'color': COLORS['dark_gray']
    },
    'body': {
        'family': 'Arial, Segoe UI, Malgun Gothic, sans-serif',
        'size': 11,
        'weight': 'normal',
        'color': COLORS['dark_gray']
    },
    'label': {
        'family': 'Arial, Segoe UI, sans-serif',
        'size': 9,
        'weight': 'normal',
        'color': COLORS['dark_gray']
    }
}

# Plotly 차트 기본 레이아웃
PLOTLY_LAYOUT = {
    'paper_bgcolor': COLORS['white'],
    'plot_bgcolor': COLORS['white'],
    'font': {
        'family': FONTS['body']['family'],
        'size': FONTS['body']['size'],
        'color': FONTS['body']['color']
    },
    'margin': {'l': 60, 'r': 40, 't': 60, 'b': 60},
    'hovermode': 'closest',
    'hoverlabel': {
        'bgcolor': COLORS['white'],
        'font_size': FONTS['label']['size'],
        'font_family': FONTS['label']['family']
    }
}

# 보고서 제목 및 메타데이터
REPORT_CONFIG = {
    'title': '판매 데이터 분석 보고서',
    'currency_symbol': '₩',
    'date_format': '%Y년 %m월 %d일',
    'month_format': '%m월',
    'number_format': '{:,.0f}',
    'percent_format': '{:.1f}%',
    'decimal_format': '{:,.2f}'
}

