#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KPI 분석 모듈
대시보드 개요에 표시될 주요 지표를 계산합니다.
"""

import pandas as pd
import numpy as np
from config import COLORS, REPORT_CONFIG


class KPIAnalyzer:
    """KPI(핵심성과지표) 분석 클래스"""
    
    def __init__(self, df):
        """
        Args:
            df: 판매 데이터프레임
        """
        self.df = df
        self.kpis = {}
    
    def calculate_all_kpis(self):
        """모든 KPI를 계산합니다."""
        self.kpis = {
            'total_sales': self._calculate_total_sales(),
            'total_transactions': self._calculate_total_transactions(),
            'avg_transaction': self._calculate_avg_transaction(),
            'total_discount': self._calculate_total_discount(),
            'customer_count': self._calculate_customer_count(),
            'avg_discount_rate': self._calculate_avg_discount_rate(),
            'total_quantity': self._calculate_total_quantity(),
            'unique_products': self._calculate_unique_products(),
        }
        return self.kpis
    
    def _calculate_total_sales(self):
        """총 매출액을 계산합니다."""
        total = self.df['금액'].sum()
        return {
            'value': total,
            'formatted': f"{REPORT_CONFIG['currency_symbol']}{total:,.0f}",
            'label': '총 매출액'
        }
    
    def _calculate_total_transactions(self):
        """총 거래 건수를 계산합니다."""
        count = len(self.df)
        return {
            'value': count,
            'formatted': f"{count:,}건",
            'label': '총 거래 건수'
        }
    
    def _calculate_avg_transaction(self):
        """평균 거래 금액을 계산합니다."""
        avg = self.df['금액'].mean()
        return {
            'value': avg,
            'formatted': f"{REPORT_CONFIG['currency_symbol']}{avg:,.0f}",
            'label': '평균 거래 금액'
        }
    
    def _calculate_total_discount(self):
        """총 할인액을 계산합니다."""
        if '할인액' in self.df.columns:
            total = self.df['할인액'].sum()
        else:
            total = 0
        return {
            'value': total,
            'formatted': f"{REPORT_CONFIG['currency_symbol']}{total:,.0f}",
            'label': '총 할인액'
        }
    
    def _calculate_customer_count(self):
        """거래처 수를 계산합니다."""
        count = self.df['거래처명'].nunique()
        return {
            'value': count,
            'formatted': f"{count:,}개",
            'label': '거래처 수'
        }
    
    def _calculate_avg_discount_rate(self):
        """평균 할인율을 계산합니다."""
        if 'Discount' in self.df.columns:
            avg_rate = self.df[self.df['Discount'] > 0]['Discount'].mean() * 100
            if pd.isna(avg_rate):
                avg_rate = 0
        else:
            avg_rate = 0
        return {
            'value': avg_rate,
            'formatted': f"{avg_rate:.1f}%",
            'label': '평균 할인율'
        }
    
    def _calculate_total_quantity(self):
        """총 판매 수량을 계산합니다."""
        total = self.df['수량'].sum()
        return {
            'value': total,
            'formatted': f"{total:,.0f}개",
            'label': '총 판매 수량'
        }
    
    def _calculate_unique_products(self):
        """판매된 제품 종류를 계산합니다."""
        count = self.df['제품명'].nunique()
        return {
            'value': count,
            'formatted': f"{count:,}종",
            'label': '제품 종류'
        }
    
    def get_kpis(self):
        """계산된 KPI를 반환합니다."""
        if not self.kpis:
            self.calculate_all_kpis()
        return self.kpis
    
    def get_kpi_summary(self):
        """KPI 요약 정보를 반환합니다."""
        kpis = self.get_kpis()
        return {
            'main_kpis': [
                kpis['total_sales'],
                kpis['total_transactions'],
                kpis['avg_transaction'],
                kpis['total_discount'],
            ],
            'sub_kpis': [
                kpis['customer_count'],
                kpis['avg_discount_rate'],
                kpis['total_quantity'],
                kpis['unique_products'],
            ]
        }

