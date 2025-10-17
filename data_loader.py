#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 로더 모듈
판매 데이터를 읽고 전처리하는 기능을 제공합니다.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys


class SalesDataLoader:
    """판매 데이터를 로드하고 전처리하는 클래스"""
    
    def __init__(self, file_path='판매.xlsx', sheet_name='판매'):
        """
        Args:
            file_path: 엑셀 파일 경로
            sheet_name: 시트명
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.df = None
        self.data_info = {}
        
    def load_data(self):
        """데이터를 로드하고 기본 전처리를 수행합니다."""
        try:
            # 엑셀 파일 읽기
            self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            
            # 컬럼명 정리 (공백 제거)
            self.df.columns = self.df.columns.str.strip()
            
            # 날짜 컬럼을 datetime으로 변환
            if '날짜' in self.df.columns:
                self.df['날짜'] = pd.to_datetime(self.df['날짜'])
                
            # 파생 컬럼 생성
            self._create_derived_columns()
            
            # 데이터 정보 수집
            self._collect_data_info()
            
            print(f"✓ 데이터 로드 완료: {len(self.df)}건")
            return self.df
            
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {self.file_path}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 데이터 로드 중 오류 발생: {e}")
            sys.exit(1)
    
    def _create_derived_columns(self):
        """파생 컬럼을 생성합니다."""
        if '날짜' in self.df.columns:
            # 년, 월, 분기, 요일 추출
            self.df['년'] = self.df['날짜'].dt.year
            self.df['월'] = self.df['날짜'].dt.month
            self.df['분기'] = self.df['날짜'].dt.quarter
            self.df['요일'] = self.df['날짜'].dt.day_name()
            self.df['년월'] = self.df['날짜'].dt.to_period('M').astype(str)
            
            # 한글 요일명
            요일_매핑 = {
                'Monday': '월요일',
                'Tuesday': '화요일',
                'Wednesday': '수요일',
                'Thursday': '목요일',
                'Friday': '금요일',
                'Saturday': '토요일',
                'Sunday': '일요일'
            }
            self.df['요일명'] = self.df['요일'].map(요일_매핑)
        
        # 할인율 계산 (Discount가 비율인 경우)
        if 'Discount' in self.df.columns:
            self.df['할인율'] = self.df['Discount'] * 100
            
        # 할인액 계산
        if '단가' in self.df.columns and '수량' in self.df.columns and 'Discount' in self.df.columns:
            self.df['할인전금액'] = self.df['단가'] * self.df['수량']
            self.df['할인액'] = self.df['할인전금액'] * self.df['Discount']
            
        # 할인 적용 여부
        if 'Discount' in self.df.columns:
            self.df['할인적용'] = self.df['Discount'].apply(lambda x: '할인' if x > 0 else '정상가')
    
    def _collect_data_info(self):
        """데이터의 기본 정보를 수집합니다."""
        self.data_info = {
            '총_거래건수': len(self.df),
            '데이터_시작일': self.df['날짜'].min() if '날짜' in self.df.columns else None,
            '데이터_종료일': self.df['날짜'].max() if '날짜' in self.df.columns else None,
            '컬럼_목록': list(self.df.columns),
            '거래처_수': self.df['거래처명'].nunique() if '거래처명' in self.df.columns else 0,
            '제품_수': self.df['제품명'].nunique() if '제품명' in self.df.columns else 0,
            '제품분류_수': self.df['분류명'].nunique() if '분류명' in self.df.columns else 0,
        }
    
    def get_data(self):
        """로드된 데이터프레임을 반환합니다."""
        if self.df is None:
            self.load_data()
        return self.df
    
    def get_data_info(self):
        """데이터 정보를 반환합니다."""
        if not self.data_info:
            self.load_data()
        return self.data_info
    
    def validate_data(self):
        """데이터의 유효성을 검증합니다."""
        required_columns = ['날짜', '거래처명', '분류명', '제품명', '단가', '수량', '금액']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            print(f"⚠ 필수 컬럼 누락: {', '.join(missing_columns)}")
            return False
        
        # 결측치 확인
        null_counts = self.df[required_columns].isnull().sum()
        if null_counts.sum() > 0:
            print(f"⚠ 결측치 발견:")
            for col, count in null_counts[null_counts > 0].items():
                print(f"  - {col}: {count}건")
        
        print("✓ 데이터 검증 완료")
        return True


if __name__ == '__main__':
    # 테스트 코드
    loader = SalesDataLoader()
    df = loader.load_data()
    loader.validate_data()
    
    print("\n=== 데이터 정보 ===")
    for key, value in loader.get_data_info().items():
        print(f"{key}: {value}")
    
    print("\n=== 데이터 샘플 ===")
    print(df.head())

