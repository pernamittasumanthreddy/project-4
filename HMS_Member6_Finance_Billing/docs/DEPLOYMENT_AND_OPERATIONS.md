# Deployment & Operations Guide — Member 6 Pod

**Project:** Hospital Management System (HMS) — Multi-Tenant SaaS  
**Pod:** Member 6 — Billing, Payments, Insurance, Taxes, and Accounting  

---

## 1. Local Development Runbook

### Backend (Django + DRF)
```bash
# 1. Activate Python virtual environment
.\venv\Scripts\Activate.ps1

# 2. Apply database migrations
python backend/manage.py migrate

# 3. Seed financial master catalogue, tax slabs, chart of accounts & sample invoices
python backend/manage.py seed_finance_data

# 4. Run automated test suite (13 comprehensive tests)
pytest -v

# 5. Start development API server (Port 8000)
python backend/manage.py runserver 127.0.0.1:8000
```

### Frontend (React + Vite + TypeScript)
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm.cmd install

# 3. Compile and build validation
npm.cmd run build

# 4. Launch Vite development server (Port 5173)
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

---

## 2. Docker & Containerized Deployment

```bash
# Build and run backend + frontend containers
docker-compose up --build -d

# Check running services
docker-compose ps
```

---

## 3. OpenAPI Documentation
Once the backend is running, the interactive Swagger UI and OpenAPI 3.0 schema are available at:
- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **OpenAPI Schema:** `http://127.0.0.1:8000/api/schema/`
