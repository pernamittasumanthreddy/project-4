Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Launching CareTrust HMS Enterprise Platform (Member 7 Portal Suite)" -ForegroundColor Green
Write-Host "Zero External API Keys Required - 100% Local Execution" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "`n[1/3] Applying Database Migrations..." -ForegroundColor Gray
python backend\manage.py migrate

Write-Host "`n[2/3] Seeding Multi-Tenant Personas and Clinical Encounters..." -ForegroundColor Gray
python backend\seed_hms_data.py

Write-Host "`n[3/3] Starting Django Backend and Vite Frontend..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python backend\manage.py runserver 127.0.0.1:8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "Both servers launched successfully!" -ForegroundColor Green
Write-Host "Frontend Portal: http://localhost:5173" -ForegroundColor White
Write-Host "Backend API:     http://127.0.0.1:8000/api/v1/health/" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
