"""
Offer and Placement Domain Models
Tracks offer parameters, candidate acceptance, joining status, and final placement confirmation
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Offer:
    offer_id: Optional[int] = None
    offer_code: str = ""
    application_id: int = 0
    candidate_id: int = 0
    company_id: int = 0
    job_id: int = 0
    offered_role: str = ""
    offered_package: float = 0.0  # LPA
    offer_date: Optional[date] = None
    expected_joining_date: Optional[date] = None
    status: str = "OFFERED"  # OFFERED, ACCEPTED, REJECTED, EXPIRED, WITHDRAWN
    remarks: str = ""

@dataclass
class Placement:
    placement_id: Optional[int] = None
    placement_code: str = ""
    offer_id: int = 0
    candidate_id: int = 0
    company_id: int = 0
    job_id: int = 0
    designation: str = ""
    package_offered: float = 0.0
    actual_joining_date: Optional[date] = None
    joining_status: str = "JOINED"  # JOINED, NOT_JOINED, DEFERRED, NO_SHOW
    corporate_emp_id: str = ""
    placement_officer: str = "Neha Deshmukh"
    remarks: str = ""
