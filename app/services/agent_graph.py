from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from app.services.insight_agent import build_management_report

class BusinessState(TypedDict, total=False):
    metrics: dict[str, Any]
    anomalies: list[dict[str, Any]]
    bottlenecks: list[dict[str, Any]]
    question: str
    performance_findings: list[str]
    risk_findings: list[str]
    workflow_findings: list[str]
    report: str
    agent_trace: list[str]

def performance_agent(state: BusinessState):
    m = state["metrics"]
    findings = [
        f"Revenue is {m['total_revenue']:,.2f}.",
        f"Expenses are {m['total_expenses']:,.2f}; net after expenses is {m['net_after_expenses']:,.2f}.",
        f"Active employee count is {m['active_employees']}."
    ]
    return {"performance_findings": findings,
            "agent_trace": state.get("agent_trace", []) + ["Performance Analyst Agent"]}

def risk_agent(state: BusinessState):
    anomalies = state.get("anomalies", [])
    findings = [f"{len(anomalies)} expense records were flagged for human review."]
    findings += [f"High-value flagged expense: {a.get('vendor')} / {a.get('category')} / {a.get('amount')}."
                 for a in anomalies[:3]]
    return {"risk_findings": findings,
            "agent_trace": state.get("agent_trace", []) + ["Financial Risk Agent"]}

def workflow_agent(state: BusinessState):
    bottlenecks = state.get("bottlenecks", [])
    slow = [b for b in bottlenecks if b.get("is_bottleneck")]
    findings = [f"{len(slow)} workflow stages are above the bottleneck threshold."]
    findings += [f"{b['stage']} averages {b['avg_duration_hours']} hours."
                 for b in slow[:3]]
    return {"workflow_findings": findings,
            "agent_trace": state.get("agent_trace", []) + ["Workflow Optimization Agent"]}

def executive_agent(state: BusinessState):
    report = build_management_report(state["metrics"], state.get("anomalies", []),
                                     state.get("bottlenecks", []), state.get("question", ""))
    return {"report": report,
            "agent_trace": state.get("agent_trace", []) + ["Executive Synthesis Agent"]}

builder = StateGraph(BusinessState)
builder.add_node("performance", performance_agent)
builder.add_node("risk", risk_agent)
builder.add_node("workflow", workflow_agent)
builder.add_node("executive", executive_agent)
builder.add_edge(START, "performance")
builder.add_edge("performance", "risk")
builder.add_edge("risk", "workflow")
builder.add_edge("workflow", "executive")
builder.add_edge("executive", END)
business_agent_graph = builder.compile()

def run_business_agents(metrics, anomalies, bottlenecks, question):
    result = business_agent_graph.invoke({
        "metrics": metrics, "anomalies": anomalies, "bottlenecks": bottlenecks,
        "question": question, "agent_trace": []
    })
    return {"report": result["report"], "agent_trace": result["agent_trace"],
            "findings": {
                "performance": result.get("performance_findings", []),
                "risk": result.get("risk_findings", []),
                "workflow": result.get("workflow_findings", [])
            }}
