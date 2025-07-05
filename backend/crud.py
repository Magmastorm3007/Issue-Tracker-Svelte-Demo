from sqlalchemy.orm import Session
from models import User, Issue, DailyStats
from schemas import UserCreate, IssueCreate, IssueUpdate
from passlib.context import CryptContext
from datetime import date

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------ USER ------------------

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, hashed_pw: str = None):
    if not hashed_pw:
        hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ------------------ ISSUE ------------------

def get_issues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Issue).offset(skip).limit(limit).all()


def get_issue(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()


def create_issue(db: Session, issue: IssueCreate, reporter_id: int):
    db_issue = Issue(
        title=issue.title,
        description=issue.description,
        severity=issue.severity,
        status="OPEN",
        reporter_id=reporter_id
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def update_issue(db: Session, issue_id: int, issue_update: IssueUpdate):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        return None
    for key, value in issue_update.dict(exclude_unset=True).items():
        setattr(db_issue, key, value)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def delete_issue(db: Session, issue_id: int):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue:
        db.delete(db_issue)
        db.commit()
    return db_issue


# ------------------ DAILY STATS ------------------

def save_daily_stats(db: Session, stats_dict: dict):
    today = date.today()
    existing = db.query(DailyStats).filter(DailyStats.date == today).first()

    if not existing:
        daily_stat = DailyStats(
            date=today,
            open_count=stats_dict.get("OPEN", 0),
            triaged_count=stats_dict.get("TRIAGED", 0),
            in_progress_count=stats_dict.get("IN_PROGRESS", 0),
            done_count=stats_dict.get("DONE", 0)
        )
        db.add(daily_stat)
    else:
        existing.open_count = stats_dict.get("OPEN", 0)
        existing.triaged_count = stats_dict.get("TRIAGED", 0)
        existing.in_progress_count = stats_dict.get("IN_PROGRESS", 0)
        existing.done_count = stats_dict.get("DONE", 0)
    
    db.commit()
