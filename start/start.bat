@echo off
title AHADU PULSE - Launcher
color 0A
chcp 65001 >nul 2>&1

setlocal

REM ==================================================
REM Paths
REM ==================================================

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%..\backend"
set "FRONTEND_DIR=%SCRIPT_DIR%..\frontend"

echo.
echo ==================================================
echo   AHADU BANK - AHADU PULSE v1.0.0
echo   AI-Powered Digital Banking Evaluation Platform
echo ==================================================
echo.

echo SCRIPT_DIR=%SCRIPT_DIR%
echo BACKEND_DIR=%BACKEND_DIR%
echo FRONTEND_DIR=%FRONTEND_DIR%
echo.

REM ==================================================
REM Check Python
REM ==================================================

where py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python launcher not found.
    echo Install Python 3.11+ and add it to PATH.
    pause
    exit /b 1
)

echo [OK] Python found.

REM ==================================================
REM Check Node.js
REM ==================================================

where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found.
    echo Install Node.js 18+.
    pause
    exit /b 1
)

echo [OK] Node.js found.

REM ==================================================
REM Check MySQL
REM ==================================================

echo.
echo [..] Checking MySQL...

py "%SCRIPT_DIR%check_mysql.py"

if errorlevel 1 (
    echo.
    echo [WARNING] MySQL is not running.
    echo Start MySQL from XAMPP or MySQL Service.
    echo.

    choice /C YN /T 10 /D Y /M "Continue anyway?"

    if errorlevel 2 (
        exit /b 0
    )
)

REM ==================================================
REM Backend Dependencies
REM ==================================================

echo.
echo [..] Checking backend packages...

py "%SCRIPT_DIR%check_deps.py"

if errorlevel 1 (
    echo [..] Installing backend packages...

    py -m pip install -r "%BACKEND_DIR%\requirements.txt"

    if errorlevel 1 (
        echo [ERROR] Backend dependency installation failed.
        pause
        exit /b 1
    )

    echo [OK] Backend packages installed.
) else (
    echo [OK] Backend packages ready.
)

REM ==================================================
REM Frontend Dependencies
REM ==================================================

echo.
echo [..] Checking frontend packages...

py "%SCRIPT_DIR%check_frontend.py"

if errorlevel 1 (
    echo [..] Installing frontend packages...

    pushd "%FRONTEND_DIR%"
    call npm install

    if errorlevel 1 (
        popd
        echo [ERROR] Frontend dependency installation failed.
        pause
        exit /b 1
    )

    popd

    echo [OK] Frontend packages installed.
) else (
    echo [OK] Frontend packages ready.
)

REM ==================================================
REM Launch Backend
REM ==================================================

echo.
echo [..] Launching Backend...

start "AHADU Backend" cmd /k "cd /d ""%BACKEND_DIR%"" && py -m uvicorn app.main:app --reload --port 8000"

REM ==================================================
REM Wait for Backend Startup
REM ==================================================

echo [..] Waiting for backend...
timeout /t 5 /nobreak >nul

REM ==================================================
REM Launch Frontend
REM ==================================================

echo [..] Launching Frontend...

start "AHADU Frontend" cmd /k "cd /d ""%FRONTEND_DIR%"" && npm run dev"

REM ==================================================
REM Summary
REM ==================================================

echo.
echo ==================================================
echo Services Started
echo.
echo Frontend : http://localhost:3000
echo Backend  : http://localhost:8000
echo API Docs : http://localhost:8000/docs
echo.
echo Login
echo --------------------------------------------------
echo Email    : admin@ahadubank.com
echo Password : Admin@123
echo ==================================================
echo.

pause