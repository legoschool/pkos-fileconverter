@echo off
chcp 65001 >nul
cd /d "%~dp0"
where pythonw >nul 2>nul
if not errorlevel 1 (
    start "" pythonw "%~dp0pkos_app.py"
    exit /b
)
where pyw >nul 2>nul
if not errorlevel 1 (
    start "" pyw -3 "%~dp0pkos_app.py"
    exit /b
)
echo Python을 찾을 수 없습니다. Python 설치 후 아래 명령으로 의존성을 설치하세요.
echo python -m pip install -r requirements.txt
pause
