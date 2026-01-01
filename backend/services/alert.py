ALERTS = []

def trigger_alert(area_id: str, avg_risk: float, reports: int):
    alert = {
        "area_id": area_id,
        "avg_risk": round(avg_risk, 2),
        "reports": reports,
        "message": "High flood risk detected",
    }

    ALERTS.append(alert)
    print("🚨 ALERT:", alert)
