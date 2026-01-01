from fastapi import APIRouter
from routes.report import REPORTS

router = APIRouter()

@router.get("/")
@router.get("/")
def get_hotspots():
    heatmap_points = []

    for r in REPORTS:
        weight = r["risk_score"] / 20  # normalize for Google heatmap

        heatmap_points.append({
            "lat": r["lat"],
            "lng": r["lng"],
            "weight": weight,
            "risk": r["risk_level"]
        })

    return heatmap_points

