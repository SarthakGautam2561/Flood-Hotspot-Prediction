from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.report import router as report_router
from routes.hotspot import router as hotspot_router
from routes.data import router as data_router

app = FastAPI(
    title="Delhi Flood Watch Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

app.include_router(report_router, prefix="/report", tags=["Report"])
app.include_router(hotspot_router, prefix="/hotspots", tags=["Hotspots"])
app.include_router(data_router, prefix="/data", tags=["Dashboard"])
