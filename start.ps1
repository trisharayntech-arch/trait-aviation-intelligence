# TRAIT Aviation Intelligence - Windows PowerShell Launcher
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "         TRAIT INNOVATION - TRAIT AVIATION INTELLIGENCE v2.0" -ForegroundColor White
Write-Host "         Integrated AirportAI and Aviation Analytics Platform" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path (Join-Path $scriptDir "backend")

Write-Host "[1/2] Seeding / Verifying Synthetic Database..." -ForegroundColor Yellow
python -m app.seed_data

Write-Host "[2/2] Starting Server on http://127.0.0.1:8000 ..." -ForegroundColor Green
Start-Process "http://127.0.0.1:8000"

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
