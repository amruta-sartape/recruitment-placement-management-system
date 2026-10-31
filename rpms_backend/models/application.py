"""
Application Domain Model
Tracks candidate application pipeline status and eligibility evaluation
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Application:
    application_id: Optional[int] = None
    application_code: str = ""
    candidate_id: int = 0
    job_id: int = 0
    applied_at: Optional[datetime] = None
    status: str = "APPLIED"  # APPLIED, ELIGIBLE, SHORTLISTED, INTERVIEW_SCHEDULED, SELECTED, REJECTED, WITHDRAWN
    eligibility_status: str = "PENDING"  # ELIGIBLE, INELIGIBLE, PENDING
    eligibility_remarks: str = ""

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "application_code": self.application_code,
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "applied_at": str(self.applied_at) if self.applied_at else "",
            "status": self.status,
            "eligibility_status": self.eligibility_status,
            "eligibility_remarks": self.eligibility_remarks,
        }
