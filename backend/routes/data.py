from fastapi import APIRouter
from routes.report import REPORTS
from datetime import datetime, timedelta
from services.maps import get_area_key
from services.alert import trigger_alert
from services.alert import ALERTS
from collections import defaultdict

router = APIRouter()

@router.get("/summary")
def dashboard_summary():
    total = len(REPORTS)

    high = sum(1 for r in REPORTS if r["severity"] >= 4)
    medium = sum(1 for r in REPORTS if r["severity"] == 3)
    low = sum(1 for r in REPORTS if r["severity"] <= 2)

    return {
        "total_reports": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "response_rate": 94  # static for now
    }


@router.get("/recent")
def recent_reports():
    latest = REPORTS[-5:][::-1]

    return [
        {
            "lat": r["lat"],
            "lng": r["lng"],
            "severity": r["severity"],
            "rainfall": r["rainfall"],
            "risk_score": r["risk_score"],
            "risk_level": r["risk_level"],
            "time": r["timestamp"]
        }
        for r in latest
    ]

@router.get("/wards")
def ward_wise_risk():
    wards = {}

    for r in REPORTS:
        key = get_area_key(r["lat"], r["lng"])

        if key not in wards:
            wards[key] = {
                "count": 0,
                "risk_sum": 0,
                "lat": r["lat"],
                "lng": r["lng"]
            }

        wards[key]["count"] += 1
        wards[key]["risk_sum"] += r["risk_score"]

    result = []

    for key, w in wards.items():
        avg_risk = w["risk_sum"] / w["count"]

        if avg_risk >= 60:
            level = "high"
        elif avg_risk >= 30:
            level = "medium"
        else:
            level = "low"

        if level == "high" and w["count"] >= 3:
            trigger_alert(key, avg_risk, w["count"])

        result.append({
            "area_id": key,
            "lat": w["lat"],
            "lng": w["lng"],
            "reports": w["count"],
            "avg_risk": round(avg_risk, 2),
            "risk_level": level
        })

    return result

@router.get("/alerts")
def get_alerts():
    return ALERTS

@router.get("/ward-risk")
def get_ward_risk():
    ward_map = defaultdict(lambda: {
        "zone": "",
        "reports": 0,
        "risk": "Low",
        "updated": "Just now"
    })

    for r in REPORTS:
        ward = r.get("ward", "Unknown")
        severity = r["severity"]

        ward_map[ward]["zone"] = r.get("zone", "Unknown")
        ward_map[ward]["reports"] += 1

        if severity >= 4:
            ward_map[ward]["risk"] = "High"
        elif severity >= 2:
            ward_map[ward]["risk"] = "Medium"

        ward_map[ward]["updated"] = "Just now"

    return [
        {
            "ward": k,
            **v
        }
        for k, v in ward_map.items()
    ]