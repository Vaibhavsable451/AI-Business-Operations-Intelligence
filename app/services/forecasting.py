import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from app.models import Sale

def forecast_revenue(db, horizon=30):
    rows = db.query(Sale.date, Sale.revenue).order_by(Sale.date).all()
    if len(rows) < 14:
        return {"history": [], "forecast": [], "note": "At least 14 days of sales data are required."}
    df = pd.DataFrame([{"date":r.date, "revenue":r.revenue} for r in rows])
    daily = df.groupby("date", as_index=False)["revenue"].sum().sort_values("date")
    daily["t"] = np.arange(len(daily))
    model = LinearRegression().fit(daily[["t"]], daily["revenue"])
    future_t = np.arange(len(daily), len(daily)+horizon)
    pred = np.maximum(0, model.predict(future_t.reshape(-1,1)))
    dates = pd.date_range(pd.Timestamp(daily.date.max()) + pd.Timedelta(days=1), periods=horizon)
    return {"history":[{"date":str(r.date), "revenue":round(float(r.revenue),2)} for r in daily.itertuples()],
            "forecast":[{"date":str(d.date()), "revenue":round(float(v),2)} for d,v in zip(dates,pred)],
            "note":"Baseline linear trend forecast; use as directional planning support, not a guarantee."}
