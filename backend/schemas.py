from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import date


# Used Enums to define fixed sets of values for roles, severity, and issue status

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    REPORTER = "REPORTER"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class IssueStatus(str, Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


# -------- USER SCHEMAS --------

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


# -------- ISSUE SCHEMAS --------

class IssueBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: Severity


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    severity: Optional[Severity]
    status: Optional[IssueStatus]


class IssueOut(IssueBase):
    id: int
    status: IssueStatus
    reporter_id: int

    class Config:
        orm_mode = True


# -------- DAILY STATS --------

class DailyStatsOut(BaseModel):
    date: date
    open_count: int
    triaged_count: int
    in_progress_count: int
    done_count: int

    class Config:
        orm_mode = True
