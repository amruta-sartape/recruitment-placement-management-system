"""
Company Domain Model
Represents corporate employers and placement recruiters
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Company:
    company_id: Optional[int] = None
    company_code: str = ""
    company_name: str = ""
    industry: str = "IT Services"
    company_type: str = "MNC"
    website: str = ""
    location: str = "Pune"
    hr_name: str = ""
    hr_email: str = ""
    hr_mobile: str = ""
    status: str = "ACTIVE"

    def to_dict(self):
        return {
            "company_id": self.company_id,
            "company_code": self.company_code,
            "company_name": self.company_name,
            "industry": self.industry,
            "company_type": self.company_type,
            "website": self.website,
            "location": self.location,
            "hr_name": self.hr_name,
            "hr_email": self.hr_email,
            "hr_mobile": self.hr_mobile,
            "status": self.status,
        }
