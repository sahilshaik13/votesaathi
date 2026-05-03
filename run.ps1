# VoteSaathi Run Script
# Starts both backend (FastAPI) and frontend (Vite) for local development
Write-Host ""
Write-Host "  ==============================================" -ForegroundColor DarkCyan
Write-Host "   VoteSaathi - AI Election Assistant" -ForegroundColor Cyan
Write-Host "  ==============================================" -ForegroundColor DarkCyan
Write-Host ""

# Set environment variables
$mainCredPath = Join-Path $PSScriptRoot "credentials.json"
$firebaseCredPath = Join-Path $PSScriptRoot "votesaathi-bcf9e-firebase-adminsdk-fbsvc-c3e2b36673.json"

if (-Not (Test-Path $mainCredPath)) {
    Write-Host "  ERROR: main credentials.json not found at $mainCredPath" -ForegroundColor Red
    exit 1
}
if (-Not (Test-Path $firebaseCredPath)) {
    Write-Host "  ERROR: firebase credentials.json not found at $firebaseCredPath" -ForegroundColor Red
    exit 1
}

$env:GOOGLE_APPLICATION_CREDENTIALS = $mainCredPath
$env:FIREBASE_APPLICATION_CREDENTIALS = $firebaseCredPath
Write-Host "  Main Credentials: $mainCredPath" -ForegroundColor DarkGray
Write-Host "  Firebase Credentials: $firebaseCredPath" -ForegroundColor DarkGray

# Start Backend in a new window
Write-Host "  Starting Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:GOOGLE_APPLICATION_CREDENTIALS = '$mainCredPath'; `$env:FIREBASE_APPLICATION_CREDENTIALS = '$firebaseCredPath'; Set-Location '$PSScriptRoot\backend'; uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env"

# Start Realtime Scraper in a new window
Write-Host "  Starting Realtime Scraper (Firebase Push)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:GOOGLE_APPLICATION_CREDENTIALS = '$mainCredPath'; `$env:FIREBASE_APPLICATION_CREDENTIALS = '$firebaseCredPath'; Set-Location '$PSScriptRoot\backend'; watchmedo auto-restart --directory . --pattern '*.py' --recursive -- python live_scraper_process.py"

Write-Host "  Waiting 3 seconds for services to initialize..." -ForegroundColor DarkGray
Start-Sleep -s 3

# Start Frontend in a new window  
Write-Host "  Starting Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "  Both services starting in new PowerShell windows." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
