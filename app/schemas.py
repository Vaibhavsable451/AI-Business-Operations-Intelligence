from pydantic import BaseModel
from typing import Any

class ReportRequest(BaseModel):
    question: str = "Summarize the current business performance and recommend priorities."

class ReportResponse(BaseModel):
    report: str
    metrics: dict[str, Any]
