# One-click launch script for EXORCIST.EXE // PHANTOM
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "   EXORCIST.EXE // CYBER-NOIR OS MURDER MYSTERY          " -ForegroundColor Green
Write-Host "   Hacktoberfest 2026 Week 4: Ghost in the Machine       " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start FastAPI Backend
Write-Host "[1/2] Launching Backend on http://localhost:8000..." -ForegroundColor Cyan
$BackendCmd = "cd '$CurrentDir\backend'; & '.\.venv\Scripts\python.exe' -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
$BackendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $BackendCmd -PassThru

Start-Sleep -Seconds 2

# 2. Start Next.js Frontend
Write-Host "[2/2] Launching Next.js Web Console on http://localhost:3000..." -ForegroundColor Cyan
$FrontendCmd = "cd '$CurrentDir\frontend'; npm run dev"
$FrontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $FrontendCmd -PassThru

Write-Host ""
Write-Host ">>> Workstation Ready! Open http://localhost:3000 in your browser." -ForegroundColor Green
Write-Host ">>> Or run CLI detective directly: python backend/cli/detective.py" -ForegroundColor Yellow
Write-Host ""
