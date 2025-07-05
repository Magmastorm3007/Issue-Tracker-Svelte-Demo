from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from models import DailyStats
from models import Base
from database import engine,get_db
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)
import os
from seed_data import seed_stats

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Issues & Insights Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
if os.getenv("SEED_ON_STARTUP", "1") == "1":
    seed_stats()
@app.get("/")
def read_root():
    return {"message": "Backend up!"}
@app.get("/api/tracker-stats")
def get_tracker_stats(db: Session = Depends(get_db)):
    stats = db.query(DailyStats).order_by(DailyStats.date.asc()).all()
    return [
        {
            "date": stat.date.isoformat(),
            "open": stat.open_count,
            "triaged": stat.triaged_count
        }
        for stat in stats
    ]

