@echo off
if not exist .venv\Scripts\python.exe (
  echo Run setup_windows.ps1 first.
  pause
  exit /b 1
)
.venv\Scripts\python.exe app.py
