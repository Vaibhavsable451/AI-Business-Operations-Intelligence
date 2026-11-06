from app.database import Base, engine, SessionLocal
from app.models import Sale, Expense, Employee, WorkflowTask
from app.services.analytics import overview
from datetime import date

def test_overview_returns_expected_metrics():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Use a dedicated in-memory database in CI for full isolation if extending this test suite.
        db.query(WorkflowTask).delete()
        db.query(Employee).delete()
        db.query(Expense).delete()
        db.query(Sale).delete()
        db.add(Sale(date=date.today(), department="Sales", product="Demo", revenue=1000, units=2))
        db.add(Expense(date=date.today(), department="Sales", category="Demo", vendor="Demo", amount=250))
        db.add(Employee(name="Test", department="Sales", monthly_target=10, monthly_output=8, active=1))
        db.add(WorkflowTask(process_name="Demo", stage="Approval", duration_hours=2,
                            status="Delayed", owner_department="Sales"))
        db.commit()
        result = overview(db)
        assert result["total_revenue"] == 1000
        assert result["total_expenses"] == 250
        assert result["net_after_expenses"] == 750
        assert result["delayed_tasks"] == 1
    finally:
        db.close()
