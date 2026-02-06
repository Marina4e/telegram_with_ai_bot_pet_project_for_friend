@echo off
cd /d %~dp0

echo ==========================================
echo   Telegram GPT Bot starting...
echo ==========================================

python --version >nul 2>&1
IF ERRORLEVEL 1 (
  echo.
  echo ❌ Python не знайдено.
  echo Встанови Python 3.10+ і перезапусти.
  pause
  exit /b 1
)

IF NOT EXIST ".env" (
  echo.
  echo ❌ Файл .env не знайдено.
  echo Створи його: скопіюй .env.example -> .env
  pause
  exit /b 1
)

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Running bot...
python bot.py

pause
