@echo off
cd /d "%~dp0"
echo Запуск бота @ALIEXSPRESSSSSELLBOT...
py bot.py
if errorlevel 1 pause
