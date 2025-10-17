@echo off
chcp 65001 > nul
echo ====================================
echo 판매 데이터 분석 보고서 생성
echo ====================================
echo.

REM Python 실행 (py 명령어 사용)
py -3 generate_report.py

echo.
echo 아무 키나 눌러 종료하세요...
pause > nul

