@echo off
echo Starting AI Teaching Assistant...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Swagger: http://localhost:8000/docs
echo.
cd /d "%~dp0"

REM Start backend
start "Backend" cmd /c "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

cd frontend
REM Start frontend
start "Frontend" cmd /c "npm run dev -- --host"

echo Both servers starting...
echo Frontend will be ready at http://localhost:3000
echo Backend will be ready at http://localhost:8000
