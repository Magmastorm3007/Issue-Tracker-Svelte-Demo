from sqlalchemy.orm import Session
from datetime import date
from database import SessionLocal
from models import DailyStats

def seed_stats():
    db: Session = SessionLocal()
    
    existing = db.query(DailyStats).count()
    if existing == 0:
        stats = [
            DailyStats(date=date(2025, 7, 1), open_count=5, triaged_count=3),
            DailyStats(date=date(2025, 7, 2), open_count=4, triaged_count=2),
            DailyStats(date=date(2025, 7, 3), open_count=6, triaged_count=4),
        ]
        db.add_all(stats)
        db.commit()
        print("Seeded daily stats ✅")
    else:
        print("Daily stats already exist ✅")

    db.close()

if __name__ == "__main__":
    seed_stats()
