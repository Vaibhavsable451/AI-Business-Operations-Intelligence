from app.config import settings

def build_management_report(metrics, anomalies, bottlenecks, question):
    context = {"overview":metrics, "top_expense_anomalies":anomalies[:5],
               "workflow_bottlenecks":bottlenecks[:5], "manager_question":question}
    fallback = (
        "## Executive summary\n"
        f"- Revenue recorded: **{metrics['total_revenue']:,.2f}**; expenses: **{metrics['total_expenses']:,.2f}**.\n"
        f"- Net after recorded expenses: **{metrics['net_after_expenses']:,.2f}**.\n"
        f"- Delayed workflow tasks: **{metrics['delayed_tasks']}** "
        f"({metrics['delay_rate_pct']}% of tracked tasks).\n\n"
        "## Recommended priorities\n"
        "1. Review the highest-value expense anomalies against receipts and purchase approvals. "
        "An anomaly is a review signal, not proof of misconduct.\n"
        "2. Investigate the slowest workflow stage and measure queue time, hand-offs and approval wait time.\n"
        "3. Compare department revenue, expenses and employee target attainment before reallocating resources.\n"
        "4. Review the revenue trend forecast weekly and compare forecast with actual results.\n\n"
        "## Manager question\n" + question + "\n\n"
        "_This report is decision support based on the demo database. Validate findings before taking action._"
    )
    if not settings.groq_api_key:
        return fallback
    try:
        from groq import Groq
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.groq_model,
            temperature=0.2,
            messages=[
                {"role":"system","content":"You are a careful business operations analyst. Use only supplied metrics. Do not invent facts. Treat anomaly flags as leads for human review, not proof. Give concise, prioritized recommendations."},
                {"role":"user","content":f"Analyze this business data and answer the manager question. Return Markdown. Data: {context}"}
            ]
        )
        return response.choices[0].message.content or fallback
    except Exception as exc:
        return fallback + f"\n\n_Groq unavailable; fallback report used ({type(exc).__name__})._"
