def calculate_risk(severity: int, rainfall: float):
    score = (severity * 15) + (rainfall * 4)

    if score >= 60:
        level = "high"
    elif score >= 30:
        level = "medium"
    else:
        level = "low"

    return round(score, 2), level

def infer_zone(area: str) -> str:
    area = area.lower()

    if any(x in area for x in ["connaught", "karol", "paharganj"]):
        return "Central"
    if any(x in area for x in ["mayur", "preet", "anand vihar"]):
        return "East"
    if any(x in area for x in ["rohini", "narela"]):
        return "North"
    if any(x in area for x in ["dwarka", "janakpuri"]):
        return "South-West"

    return "Unknown"
