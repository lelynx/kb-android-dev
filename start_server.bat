@echo off
cd /d %~dp0
echo Demarrage du serveur Knowledge Base sur http://localhost:8002
echo Documentation Swagger : http://localhost:8002/docs
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
pause
