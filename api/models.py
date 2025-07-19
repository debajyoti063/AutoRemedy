from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class EventIn(BaseModel):
    job_id: int
    status: str
    event_type: str = "job_issue"
    details: Optional[Dict[str, Any]] = None

class FeedbackIn(BaseModel):
    event_id: str
    user: str
    rating: int
    comment: Optional[str] = None

class StatusOut(BaseModel):
    status: str
    detail: Optional[str] = None

class HistoryRecord(BaseModel):
    event: Dict[str, Any]
    actions: List[Dict[str, Any]]
    outcomes: List[Any]
    feedback: Optional[Dict[str, Any]] = None

class HistoryOut(BaseModel):
    records: List[HistoryRecord] 