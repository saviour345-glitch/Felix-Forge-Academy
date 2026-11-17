$ErrorActionPreference = 'Stop'
Write-Host 'Setting up FelixForge Academy...' -ForegroundColor Cyan
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) {
    $secret = & .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
    @("SECRET_KEY=$secret", 'DATABASE_URL=sqlite:///codecraft.db', 'ENABLE_CODE_RUNNER=false', 'AI_API_URL=', 'AI_API_KEY=', 'AI_MODEL=') | Set-Content .env
}
Write-Host 'Setup complete. Run .\run_windows.bat to start the site.' -ForegroundColor Green
