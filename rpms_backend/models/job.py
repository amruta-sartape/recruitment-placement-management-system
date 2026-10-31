"""
Job Requirement Domain Model
Encapsulates job opening data and candidate eligibility threshold cutoffs
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date
from rpms_backend.validators import BusinessValidator

@dataclass
class Job:
    job_id: Optional[int] = None
    job_code: str = ""
    company_id: int = 0
    job_title: str = ""
    openings: int = 1
    employment_type: str = "Full-time"
    location: str = "Pune"
    min_package: float = 3.5
    max_package: float = 5.0
    allowed_qualifications: List[str] = field(default_factory=lambda: ["BE", "BTech", "MCA"])
    min_percentage: float = 60.0
    min_passing_year: Optional[int] = 2024
    max_passing_year: Optional[int] = 2026
    max_backlogs: int = 0
    required_technology: str = "Java"
    required_skills: List[str] = field(default_factory=list)
    posted_date: Optional[date] = None
    deadline_date: Optional[date] = None
    status: str = "OPEN"

    def validate(self):
        BusinessValidator.validate_openings(self.openings)
        BusinessValidator.validate_percentage(self.min_percentage)
        BusinessValidator.validate_backlogs(self.max_backlogs)
        BusinessValidator.validate_job_packages(self.min_package, self.max_package)
        BusinessValidator.validate_job_dates(self.posted_date, self.deadline_date)

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "job_code": self.job_code,
            "company_id": self.company_id,
            "job_title": self.job_title,
            "openings": self.openings,
            "employment_type": self.employment_type,
            "location": self.location,
            "min_package": self.min_package,
            "max_package": self.max_package,
            "allowed_qualifications": self.allowed_qualifications,
            "min_percentage": self.min_percentage,
            "min_passing_year": self.min_passing_year,
            "max_passing_year": self.max_passing_year,
            "max_backlogs": self.max_backlogs,
            "required_technology": self.required_technology,
            "required_skills": self.required_skills,
            "posted_date": str(self.posted_date) if self.posted_date else "",
            "deadline_date": str(self.deadline_date) if self.deadline_date else "",
            "status": self.status,
        }
