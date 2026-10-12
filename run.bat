@echo off
title HMS Member 4 - Laboratory and Radiology Module Launcher
echo =====================================================================
echo  Multi-Tenant Hospital Management System (HMS SaaS)
echo  MEMBER 4: Laboratory Management (LIS) and Radiology Management (RIS)
echo =====================================================================
echo.

cd /d "%~dp0backend"
echo [1/3] Applying database migrations...
py manage.py migrate --noinput

echo [2/3] Seeding test tenants, patients, catalogues, and DICOM studies...
py seed_data.py

echo [3/3] Starting Django REST API engine on port 8000...
echo Open http://localhost:8000 in your browser.
start http://localhost:8000/
py manage.py runserver 127.0.0.1:8000
pause
