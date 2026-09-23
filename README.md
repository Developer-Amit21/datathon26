# Crime Intelligence & Conversational AI Platform

## Overview
This workspace contains a full-stack crime intelligence platform with:
- FastAPI backend
- SQLite-backed domain models
- RAG-style case retrieval with evidence grounding
- Conversational chat endpoint
- Analytics and forecasting endpoints
- React frontend dashboard

## Run Backend
```bash
cd backend
PYTHONPATH=/home/dev-amit/Desktop/Datathon26/backend python3.11 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

## Verify
```bash
cd backend
PYTHONPATH=/home/dev-amit/Desktop/Datathon26/backend python3.11 -m pytest -q
cd ../frontend
npm run build
```

## Demo Credentials
- Username: admin
- Password: admin
