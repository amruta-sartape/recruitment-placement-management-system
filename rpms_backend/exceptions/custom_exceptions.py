"""
RPMS Custom Exceptions
Enforces industry-oriented business validation and process constraints
"""

class RPMSException(Exception):
    """Base exception for all RPMS operations"""
    pass

class ValidationException(RPMSException):
    """Raised when field constraints or format validations fail"""
    pass

class DuplicateApplicationException(RPMSException):
    """Raised when a candidate attempts to apply for the same job more than once"""
    pass

class IneligibleCandidateException(RPMSException):
    """Raised when candidate fails eligibility criteria checks"""
    def __init__(self, message, failed_rules=None):
        super().__init__(message)
        self.failed_rules = failed_rules or []

class JobClosedException(RPMSException):
    """Raised when application is submitted to a closed or expired job drive"""
    pass

class CandidateNotFoundException(RPMSException):
    """Raised when candidate record does not exist"""
    pass

class JobNotFoundException(RPMSException):
    """Raised when job requirement does not exist"""
    pass

class CompanyNotFoundException(RPMSException):
    """Raised when company record does not exist"""
    pass

class InvalidProcessStateException(RPMSException):
    """Raised when transition between recruitment workflow stages is invalid"""
    pass
