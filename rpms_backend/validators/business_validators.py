"""
RPMS Business Validators
Ensures format, range, and business integrity for all entities
"""

import re
from datetime import date
from rpms_backend.exceptions import ValidationException

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
MOBILE_REGEX = re.compile(r"^[6-9]\d{9}$")

class BusinessValidator:

    @staticmethod
    def validate_candidate_name(name: str):
        if not name or not name.strip():
            raise ValidationException("Please enter candidate name.")
        if len(name.strip()) < 2:
            raise ValidationException("Candidate name must be at least 2 characters.")

    @staticmethod
    def validate_email(email: str):
        if not email or not EMAIL_REGEX.match(email.strip()):
            raise ValidationException("Enter a valid email address.")

    @staticmethod
    def validate_mobile(mobile: str):
        cleaned = re.sub(r"\D", "", mobile or "")
        if len(cleaned) != 10 or not MOBILE_REGEX.match(cleaned):
            raise ValidationException("Mobile number must contain 10 digits starting with 6-9.")
        return cleaned

    @staticmethod
    def validate_percentage(percentage: float):
        try:
            val = float(percentage)
        except (ValueError, TypeError):
            raise ValidationException("Percentage must be a numeric value.")
        if val < 0.0 or val > 100.0:
            raise ValidationException("Percentage must be between 0 and 100.")
        return val

    @staticmethod
    def validate_backlogs(backlogs: int):
        try:
            val = int(backlogs)
        except (ValueError, TypeError):
            raise ValidationException("Backlogs must be an integer.")
        if val < 0:
            raise ValidationException("Backlog count cannot be negative.")
        return val

    @staticmethod
    def validate_openings(openings: int):
        try:
            val = int(openings)
        except (ValueError, TypeError):
            raise ValidationException("Number of openings must be a valid integer.")
        if val <= 0:
            raise ValidationException("Number of openings must be greater than zero.")
        return val

    @staticmethod
    def validate_job_packages(min_pkg: float, max_pkg: float):
        if min_pkg is not None and max_pkg is not None:
            if float(min_pkg) > float(max_pkg):
                raise ValidationException("Minimum package cannot exceed maximum package.")

    @staticmethod
    def validate_job_dates(posted_date, deadline_date):
        if posted_date and deadline_date:
            if isinstance(posted_date, str):
                posted_date = date.fromisoformat(posted_date)
            if isinstance(deadline_date, str):
                deadline_date = date.fromisoformat(deadline_date)
            if deadline_date < posted_date:
                raise ValidationException("Application deadline cannot be before posted date.")

    @staticmethod
    def validate_interview_date(interview_date):
        if interview_date:
            if isinstance(interview_date, str):
                interview_date = date.fromisoformat(interview_date)
            if interview_date < date.today():
                raise ValidationException("Interview date cannot be in the past.")
