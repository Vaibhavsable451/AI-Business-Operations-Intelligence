from app.services.analytics import workflow_stage_stats

def find_bottlenecks(db):
    stats = workflow_stage_stats(db)
    if not stats:
        return []
    baseline = sum(x["avg_duration_hours"] for x in stats) / len(stats)
    for item in stats:
        item["vs_stage_average"] = round(item["avg_duration_hours"] - baseline, 2)
        item["is_bottleneck"] = item["avg_duration_hours"] > baseline * 1.35
        if item["is_bottleneck"]:
            item["recommendation"] = f"Review queue size, approval rules and ownership for {item['stage']}."
        else:
            item["recommendation"] = "Monitor this stage; no major delay signal in the demo data."
    return sorted(stats, key=lambda x:x["avg_duration_hours"], reverse=True)
