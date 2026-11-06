# AI Business Operations Intelligence System

A local-first business intelligence application that combines SQL analytics, anomaly detection,
revenue forecasting, workflow bottleneck analysis, and AI-generated management recommendations.

## Features
- Streamlit dashboard with KPI cards and Plotly charts
- FastAPI backend with REST endpoints
- SQLite + SQLAlchemy database (easy to switch to PostgreSQL)
- Synthetic sales, expenses, employee, and workflow data
- Revenue trend forecast (scikit-learn)
- Expense anomaly detection (Isolation Forest)
- Workflow bottleneck analysis
- Optional Groq-powered management summary; works without an API key using a deterministic fallback
- Exportable management report (Markdown)

## Architecture

```text
Streamlit UI
    |
    | HTTP
    v
FastAPI
    |
    +-- SQLAlchemy / SQLite
    |
    +-- Analytics services
    |     +-- KPI + SQL analytics
    |     +-- Revenue forecasting
    |     +-- Expense anomaly detection
    |     +-- Workflow bottleneck detection
    |
    +-- LangGraph multi-agent workflow\n          +-- Performance Analyst Agent\n          +-- Financial Risk Agent\n          +-- Workflow Optimization Agent\n          +-- Executive Synthesis Agent (optional Groq LLM)
```

## Quick start (Windows PowerShell)

```powershell
cd business_operations_intelligence
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.seed
```

Terminal 1 — API:
```powershell
uvicorn app.main:app --reload --port 8000
```

Terminal 2 — dashboard:
```powershell
streamlit run frontend/dashboard.py
```

Open:
- Dashboard: http://localhost:8501
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Optional Groq setup
Add your key to `.env`:
```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```
If no key is configured, the app still runs and creates a rule-based executive summary.

## Project structure

```text
business_operations_intelligence/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   └── services/
│       ├── __init__.py
│       ├── analytics.py
│       ├── forecasting.py
│       ├── anomaly.py
│       ├── bottlenecks.py
│       └── insight_agent.py
├── frontend/
│   └── dashboard.py
├── tests/
│   └── test_analytics.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## API endpoints
- `GET /health`
- `GET /api/overview`
- `GET /api/revenue-trend`
- `GET /api/expense-anomalies`
- `GET /api/bottlenecks`
- `GET /api/department-performance`
- `POST /api/management-report` (returns agent trace and findings)

## Notes
- The included data is synthetic demo data, not real company information.
- Anomaly detection flags unusual records for human review; it does not prove fraud.
- Recommendations are decision support. Managers should validate them before acting.
