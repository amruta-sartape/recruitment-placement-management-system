"""
Candidate Domain Model
Represents student / candidate registered in the recruitment portal
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date
from rpms_backend.validators import BusinessValidator

@dataclass
class Candidate:
    candidate_id: Optional[int] = None
    candidate_code: str = ""
    full_name: str = ""
    email: str = ""
    mobile: str = ""
    date_of_birth: Optional[date] = None
    gender: str = "Male"
    qualification: str = "BE"
    college: str = ""
    university: str = ""
    passing_year: int = 2025
    percentage: float = 0.0
    cgpa: Optional[float] = None
    backlog_count: int = 0
    primary_technology: str = "Java"
    secondary_skills: List[str] = field(default_factory=list)
    current_location: str = "Pune"
    preferred_location: str = "Pune"
    profile_status: str = "ACTIVE"
    placement_status: str = "NOT_PLACED"

    def validate(self):
        """Executes full domain constraint validation"""
        BusinessValidator.validate_candidate_name(self.full_name)
        BusinessValidator.validate_email(self.email)
        self.mobile = BusinessValidator.validate_mobile(self.mobile)
        self.percentage = BusinessValidator.validate_percentage(self.percentage)
        self.backlog_count = BusinessValidator.validate_backlogs(self.backlog_count)

    def to_dict(self):
        return {
            "candidate_id": self.candidate_id,
            "candidate_code": self.candidate_code,
            "full_name": self.full_name,
            "email": self.email,
            "mobile": self.mobile,
            "qualification": self.qualification,
            "college": self.college,
            "university": self.university,
            "passing_year": self.passing_year,
            "percentage": self.percentage,
            "backlog_count": self.backlog_count,
            "primary_technology": self.primary_technology,
            "secondary_skills": ", ".join(self.secondary_skills) if isinstance(self.secondary_skills, list) else str(self.secondary_skills),
            "current_location": self.current_location,
            "preferred_location": self.preferred_location,
            "profile_status": self.profile_status,
            "placement_status": self.placement_status,
        }
