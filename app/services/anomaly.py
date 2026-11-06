import pandas as pd
from sklearn.ensemble import IsolationForest
from app.models import Expense

def detect_expense_anomalies(db):
    rows = db.query(Expense).all()
    if len(rows) < 10:
        return []
    df = pd.DataFrame([{"id":r.id,"date":str(r.date),"department":r.department,
                        "category":r.category,"vendor":r.vendor,"amount":r.amount} for r in rows])
    model = IsolationForest(contamination=0.04, random_state=42)
    df["anomaly"] = model.fit_predict(df[["amount"]])
    df["anomaly_score"] = model.decision_function(df[["amount"]])
    flagged = df[df.anomaly == -1].sort_values("amount", ascending=False)
    return flagged.drop(columns=["anomaly"]).round(3).to_dict(orient="records")
