from fastapi import APIRouter
from datetime import datetime
from services.weather import get_rainfall
from services.ml_logic import calculate_risk, infer_zone
from services.maps import get_area_name

router = APIRouter()

# GLOBAL store (used by hotspot.py also)
REPORTS = []

@router.post("/")
def submit_report(report: dict):
    rainfall = get_rainfall(report["lat"], report["lng"])
    score, level = calculate_risk(report["severity"], rainfall)

    # 📍 Area + Zone (NEW)
    ward = get_area_name(report["lat"], report["lng"])
    zone = infer_zone(ward)

    entry = {
        "lat": report["lat"],
        "lng": report["lng"],
        "severity": report["severity"],
        "rainfall": rainfall,
        "risk_score": score,
        "risk_level": level,
        "ward": ward,
        "zone": zone,
        "timestamp": datetime.utcnow().isoformat()
    }

    REPORTS.append(entry)

    return {
        "success": True,
        "risk_score": score,
        "risk_level": level,
        "rainfall_mm": rainfall,
        "ward": ward,
        "zone": zone
    }

@router.get("/")
def get_all_reports():
    return REPORTS
