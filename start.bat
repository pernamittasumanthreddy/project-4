@echo off
title HMS Enterprise Multi-Tenant SaaS Platform
echo ======================================================================
echo Launching CareTrust HMS Enterprise Platform (Multi-Tenant Suite)
echo Zero External API Keys Required - 100%% Local Execution
echo ======================================================================

echo.
echo [1/3] Applying Database Migrations...
python backend\manage.py migrate

echo.
echo [2/3] Seeding Multi-Tenant Personas, LIS/RIS and Clinical Encounters...
python backend\seed_enterprise_data.py
python backend\seed_data.py

echo.
echo [3/3] Starting Django Backend & Vite Frontend Development Servers...
start "HMS Backend (Django 6)" cmd /k "python backend\manage.py runserver 127.0.0.1:8000"
start "HMS Frontend (React Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================================================
echo Both servers started!
echo Frontend: http://localhost:5173
echo Backend API Docs: http://127.0.0.1:8000/api/docs/
echo LIS/RIS Console:  http://127.0.0.1:8000/lis-ris/
echo ======================================================================
pause
