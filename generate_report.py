#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
판매 데이터 분석 보고서 생성 스크립트

사용법:
    python generate_report.py
    또는
    py -3 generate_report.py
"""

import os
import sys
from datetime import datetime

# 모듈 임포트
from data_loader import SalesDataLoader
from analyzers import (
    KPIAnalyzer,
    TimeSeriesAnalyzer,
    ProductAnalyzer,
    CustomerAnalyzer,
    DiscountAnalyzer
)
from report_generator import ReportGenerator


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("판매 데이터 분석 보고서 생성 시작")
    print("=" * 80)
    print()
    
    # 1. 데이터 로드
    print("📂 1단계: 데이터 로드 중...")
    loader = SalesDataLoader('판매.xlsx', 'Sheet1')
    df = loader.load_data()
    
    # 데이터 검증
    if not loader.validate_data():
        print("❌ 데이터 검증 실패. 종료합니다.")
        sys.exit(1)
    
    data_info = loader.get_data_info()
    print()
    
    # 2. 데이터 분석
    print("📊 2단계: 데이터 분석 중...")
    
    # KPI 분석
    print("  - KPI 분석...")
    kpi_analyzer = KPIAnalyzer(df)
    kpis = kpi_analyzer.get_kpi_summary()
    
    # 시계열 분석
    print("  - 시계열 분석...")
    timeseries_analyzer = TimeSeriesAnalyzer(df)
    
    # 제품 분석
    print("  - 제품 분석...")
    product_analyzer = ProductAnalyzer(df)
    
    # 거래처 분석
    print("  - 거래처 분석...")
    customer_analyzer = CustomerAnalyzer(df)
    
    # 할인 분석
    print("  - 할인 분석...")
    discount_analyzer = DiscountAnalyzer(df)
    
    print("✓ 분석 완료")
    print()
    
    # 3. 보고서 생성
    print("📝 3단계: 보고서 생성 중...")
    
    analyzers = {
        'timeseries': timeseries_analyzer,
        'product': product_analyzer,
        'customer': customer_analyzer,
        'discount': discount_analyzer
    }
    
    report_gen = ReportGenerator(data_info, kpis, analyzers)
    report_gen.generate_html()
    
    # 4. 보고서 저장
    # output 디렉토리 생성
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 파일명에 날짜 포함
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'sales_report_{timestamp}.html')
    
    report_gen.save_report(output_path)
    
    # 5. 완료
    print()
    print("=" * 80)
    print("✅ 보고서 생성 완료!")
    print(f"📁 저장 위치: {os.path.abspath(output_path)}")
    print("=" * 80)
    print()
    
    # 요약 정보 출력
    print("📋 보고서 요약")
    print("-" * 80)
    print(f"데이터 기간: {data_info['데이터_시작일'].strftime('%Y-%m-%d')} ~ {data_info['데이터_종료일'].strftime('%Y-%m-%d')}")
    print(f"총 거래 건수: {data_info['총_거래건수']:,}건")
    print(f"거래처 수: {data_info['거래처_수']:,}개")
    print(f"제품 종류: {data_info['제품_수']:,}종")
    print()
    
    # KPI 주요 지표 출력
    print("💡 주요 지표")
    print("-" * 80)
    for kpi in kpis['main_kpis']:
        print(f"{kpi['label']}: {kpi['formatted']}")
    print()
    
    print("보고서 파일을 브라우저에서 열어 확인하세요.")
    print()
    
    return output_path


if __name__ == '__main__':
    try:
        output_path = main()
        
        # Windows에서 자동으로 브라우저 열기 (선택사항)
        try:
            import webbrowser
            print("브라우저에서 보고서를 여는 중...")
            webbrowser.open(os.path.abspath(output_path))
        except:
            pass
            
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

