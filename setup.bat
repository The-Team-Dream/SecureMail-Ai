@echo off
chcp 65001 > nul

:: ═══════════════════════════════════════════════════════════════
:: SecureMail-Ai — Standalone Setup Script (Windows)
:: Usage: Double-click setup.bat OR run in terminal
:: ═══════════════════════════════════════════════════════════════

set REPO_URL=https://github.com/The-Team-Dream/SecureMail-Ai

echo.
echo +==========================================+
echo ^|        SecureMail-Ai Setup              ^|
echo +==========================================+
echo.

:: ── 1. Check Docker ────────────────────────────────────────────
docker info > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is running
echo.

:: ── 2. Create .env.standalone from example ─────────────────────
if not exist .env.standalone (
    copy .env.standalone.example .env.standalone > nul
    echo [OK] Created .env.standalone
) else (
    echo [INFO] .env.standalone already exists -- skipping copy
)
echo.

:: ── 3. Ask for Groq API Key ────────────────────────────────────
echo ------------------------------------------
echo   GROQ API KEY SETUP
echo ------------------------------------------
echo.
echo   The AI service requires a Groq API key.
echo   Get one free at: https://console.groq.com/keys
echo.
echo   Press Enter to skip (service will start
echo   but analysis will fail without a key)
echo.
set /p groq_key="  Groq API Key: "

if "%groq_key%"=="" (
    echo.
    echo   [WARNING] No key provided -- AI analysis will not work
    echo             Fill GROQ_API_KEY in .env.standalone later
) else (
    powershell -Command "(Get-Content .env.standalone) -replace '^GROQ_API_KEY=.*', 'GROQ_API_KEY=%groq_key%' | Set-Content .env.standalone"
    echo   [OK] Groq API key written to .env.standalone
)
echo.

:: ── 4. Optional config reminder ────────────────────────────────
echo ------------------------------------------
echo   OPTIONAL CONFIG (defaults are fine)
echo ------------------------------------------
echo.
echo   AI_MAX_CONCURRENT=4       Max parallel analyses
echo   AI_MAX_BODY_CHARS=120000  Max email body size
echo   LOG_LEVEL=INFO
echo.
echo   Edit .env.standalone to change these.
echo.
echo   Full guide: %REPO_URL%#readme
echo.
echo ------------------------------------------
echo.
pause

:: ── 5. Start Docker Compose ────────────────────────────────────
echo.
echo [START] Starting SecureMail-Ai...
echo.
docker compose down > nul 2>&1
docker compose up --build -d

:: ── 6. Wait for service ────────────────────────────────────────
echo.
echo [WAIT] Waiting for AI service to be ready...
set RETRIES=20

:waitloop
docker compose logs ai 2>&1 | findstr /i "gRPC listening" > nul
if not errorlevel 1 goto done

set /a RETRIES-=1
if %RETRIES%==0 (
    echo.
    echo [ERROR] AI service failed to start. Check logs with:
    echo         docker compose logs ai
    pause
    exit /b 1
)
echo   still waiting...
timeout /t 3 /nobreak > nul
goto waitloop

:: ── 7. Done ────────────────────────────────────────────────────
:done
echo.
echo +==========================================+
echo ^|      OK  AI Service is running!        ^|
echo +==========================================+
echo ^|  gRPC: localhost:50051                 ^|
echo +==========================================+
echo ^|  Logs:  docker compose logs -f ai     ^|
echo ^|  Stop:  docker compose down           ^|
echo +==========================================+
echo.
pause
