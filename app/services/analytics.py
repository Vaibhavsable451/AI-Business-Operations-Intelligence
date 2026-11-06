import pandas as pd
from sqlalchemy import func
from app.models import Sale, Expense, Employee, WorkflowTask

def overview(db):
    revenue = db.query(func.coalesce(func.sum(Sale.revenue), 0)).scalar()
    expenses = db.query(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    employees = db.query(func.count(Employee.id)).filter(Employee.active == 1).scalar()
    tasks = db.query(func.count(WorkflowTask.id)).scalar()
    delayed = db.query(func.count(WorkflowTask.id)).filter(WorkflowTask.status == "Delayed").scalar()
    return {"total_revenue": round(float(revenue),2), "total_expenses": round(float(expenses),2),
            "net_after_expenses": round(float(revenue-expenses),2), "active_employees": employees,
            "workflow_tasks": tasks, "delayed_tasks": delayed,
            "delay_rate_pct": round((delayed/tasks*100) if tasks else 0,1)}

def revenue_by_month(db):
    rows = db.query(Sale.date, Sale.revenue, Sale.department).order_by(Sale.date).all()
    df = pd.DataFrame([{"date":r.date, "revenue":r.revenue, "department":r.department} for r in rows])
    if df.empty: return []
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    out = df.groupby(["month","department"], as_index=False)["revenue"].sum()
    return out.round(2).to_dict(orient="records")

def department_performance(db):
    sales = db.query(Sale.department, func.sum(Sale.revenue)).group_by(Sale.department).all()
    expenses = db.query(Expense.department, func.sum(Expense.amount)).group_by(Expense.department).all()
    emp = db.query(Employee.department, func.avg(Employee.monthly_output / Employee.monthly_target * 100),
                   func.count(Employee.id)).filter(Employee.active == 1).group_by(Employee.department).all()
    e_map = {d: float(v or 0) for d,v in expenses}
    p_map = {d: (float(avg or 0), count) for d,avg,count in emp}
    return [{"department":d, "revenue":round(float(r or 0),2), "expenses":round(e_map.get(d,0),2),
             "employee_target_attainment_pct":round(p_map.get(d,(0,0))[0],1),
             "employees":p_map.get(d,(0,0))[1]} for d,r in sales]

def workflow_stage_stats(db):
    rows = db.query(WorkflowTask.stage, func.avg(WorkflowTask.duration_hours),
                    func.count(WorkflowTask.id)).group_by(WorkflowTask.stage).all()
    return [{"stage":s, "avg_duration_hours":round(float(avg or 0),2), "task_count":n}
            for s,avg,n in rows]
