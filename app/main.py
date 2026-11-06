from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.schemas import ReportRequest
from app.services.analytics import overview, revenue_by_month, department_performance
from app.services.forecasting import forecast_revenue
from app.services.anomaly import detect_expense_anomalies
from app.services.bottlenecks import find_bottlenecks
from app.services.agent_graph import run_business_agents

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Business Operations Intelligence API", version="1.0.0",
              description="Local-first AI business analytics demo")

@app.get("/health")
def health():
    return {"status":"ok", "service":"business-operations-intelligence"}

@app.get("/api/overview")
def get_overview(db: Session = Depends(get_db)):
    return overview(db)

@app.get("/api/revenue-trend")
def get_revenue_trend(db: Session = Depends(get_db)):
    return revenue_by_month(db)

@app.get("/api/revenue-forecast")
def get_revenue_forecast(horizon: int = 30, db: Session = Depends(get_db)):
    return forecast_revenue(db, max(7, min(horizon, 90)))

@app.get("/api/expense-anomalies")
def get_expense_anomalies(db: Session = Depends(get_db)):
    return detect_expense_anomalies(db)

@app.get("/api/bottlenecks")
def get_bottlenecks(db: Session = Depends(get_db)):
    return find_bottlenecks(db)

@app.get("/api/department-performance")
def get_department_performance(db: Session = Depends(get_db)):
    return department_performance(db)

@app.post("/api/management-report")
def management_report(payload: ReportRequest, db: Session = Depends(get_db)):
    metrics = overview(db)
    anomalies = detect_expense_anomalies(db)
    bottlenecks = find_bottlenecks(db)
    result = run_business_agents(metrics, anomalies, bottlenecks, payload.question)
    return {"report":result["report"], "metrics":metrics,
            "agent_trace":result["agent_trace"], "findings":result["findings"]}
