"""
Interview Domain Model
Manages round scheduling, panel feedback, and selection decisions
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date, time

@dataclass
class InterviewRound:
    interview_id: Optional[int] = None
    interview_code: str = ""
    application_id: int = 0
    round_name: str = "Technical"  # Aptitude, Technical, Managerial, HR
    scheduled_date: Optional[date] = None
    scheduled_time: Optional[time] = None
    mode: str = "Online"
    interviewer_name: str = ""
    meeting_url: str = ""
    status: str = "SCHEDULED"  # SCHEDULED, COMPLETED, RESCHEDULED, NO_SHOW, CANCELLED

    # Evaluation feedback fields
    tech_rating: Optional[float] = None
    comm_rating: Optional[float] = None
    problem_rating: Optional[float] = None
    overall_rating: Optional[float] = None
    feedback_remarks: str = ""
    result: str = "PENDING"  # NEXT_ROUND, SELECTED, REJECTED, ON_HOLD

    def to_dict(self):
        return {
            "interview_id": self.interview_id,
            "interview_code": self.interview_code,
            "application_id": self.application_id,
            "round_name": self.round_name,
            "scheduled_date": str(self.scheduled_date) if self.scheduled_date else "",
            "scheduled_time": str(self.scheduled_time) if self.scheduled_time else "",
            "mode": self.mode,
            "interviewer_name": self.interviewer_name,
            "status": self.status,
            "tech_rating": self.tech_rating,
            "comm_rating": self.comm_rating,
            "problem_rating": self.problem_rating,
            "overall_rating": self.overall_rating,
            "feedback_remarks": self.feedback_remarks,
            "result": self.result,
        }
