"""
Candidate Eligibility Engine
The core rule-based validation engine specified in the Kiran Academy Abstract
"""

from typing import Dict, Any, List
from datetime import date
from rpms_backend.models import Candidate, Job
from rpms_backend.dao import ApplicationDAO
from rpms_backend.exceptions import (
    DuplicateApplicationException,
    JobClosedException,
    IneligibleCandidateException
)

class EligibilityResult:
    def __init__(self, is_eligible: bool, score: float, checklist: List[Dict[str, Any]], remarks: str):
        self.is_eligible = is_eligible
        self.score = score
        self.checklist = checklist
        self.remarks = remarks

    def to_dict(self):
        return {
            "is_eligible": self.is_eligible,
            "score": self.score,
            "checklist": self.checklist,
            "remarks": self.remarks,
        }

class CandidateEligibilityEngine:
    def __init__(self):
        self.app_dao = ApplicationDAO()

    def evaluate(self, candidate: Candidate, job: Job, raise_exception: bool = False) -> EligibilityResult:
        """
        Evaluates candidate against job requirements:
        1. Job status check (Must be OPEN)
        2. Duplicate application prevention
        3. Qualification check (Candidate qualification in job allowed qualifications)
        4. Percentage cutoff (Candidate aggregate % >= job min %)
        5. Passing year bounds (min_year <= candidate year <= max_year)
        6. Backlog criteria (Candidate backlogs <= max_backlogs allowed)
        7. Primary technology alignment
        8. Candidate profile status (Must be ACTIVE)
        """
        checklist = []
        failed_rules = []

        # 1. Job Status Check
        if job.status != "OPEN":
            failed_rules.append(f"Job drive '{job.job_code}' is currently {job.status}. Applications closed.")
            checklist.append({
                "rule": "Job Posting Status",
                "expected": "OPEN",
                "actual": job.status,
                "passed": False,
                "details": "Job is not accepting applications."
            })
            if raise_exception:
                raise JobClosedException(f"Cannot apply: Job {job.job_code} is {job.status}.")
        else:
            checklist.append({
                "rule": "Job Posting Status",
                "expected": "OPEN",
                "actual": job.status,
                "passed": True,
                "details": "Job is actively accepting applications."
            })

        # 2. Duplicate Application Check
        if candidate.candidate_id and job.job_id:
            existing = self.app_dao.get_by_candidate_and_job(candidate.candidate_id, job.job_id)
            if existing:
                msg = f"Candidate has already applied for this job (App Code: {existing.application_code})."
                failed_rules.append(msg)
                checklist.append({
                    "rule": "Duplicate Application Check",
                    "expected": "No prior application",
                    "actual": f"Existing: {existing.application_code}",
                    "passed": False,
                    "details": msg
                })
                if raise_exception:
                    raise DuplicateApplicationException(msg)
            else:
                checklist.append({
                    "rule": "Duplicate Application Check",
                    "expected": "No prior application",
                    "actual": "First time application",
                    "passed": True,
                    "details": "No duplicate record found."
                })

        # 3. Candidate Profile Status
        if candidate.profile_status != "ACTIVE":
            msg = f"Candidate profile status is {candidate.profile_status}. Only ACTIVE candidates may apply."
            failed_rules.append(msg)
            checklist.append({
                "rule": "Candidate Profile Status",
                "expected": "ACTIVE",
                "actual": candidate.profile_status,
                "passed": False,
                "details": msg
            })
        else:
            checklist.append({
                "rule": "Candidate Profile Status",
                "expected": "ACTIVE",
                "actual": candidate.profile_status,
                "passed": True,
                "details": "Candidate profile is verified active."
            })

        # 4. Qualification Match
        allowed_quals = [q.strip().upper() for q in job.allowed_qualifications]
        cand_qual = candidate.qualification.strip().upper()
        qual_passed = any(cand_qual == aq or cand_qual in aq for aq in allowed_quals)
        if not qual_passed:
            msg = f"Qualification '{candidate.qualification}' does not match allowed: {', '.join(job.allowed_qualifications)}"
            failed_rules.append(msg)
            checklist.append({
                "rule": "Educational Qualification",
                "expected": ", ".join(job.allowed_qualifications),
                "actual": candidate.qualification,
                "passed": False,
                "details": msg
            })
        else:
            checklist.append({
                "rule": "Educational Qualification",
                "expected": ", ".join(job.allowed_qualifications),
                "actual": candidate.qualification,
                "passed": True,
                "details": f"Qualification '{candidate.qualification}' matches drive requirement."
            })

        # 5. Percentage Cutoff
        if candidate.percentage < job.min_percentage:
            msg = f"Aggregate percentage ({candidate.percentage:.1f}%) is below minimum cutoff of {job.min_percentage:.1f}%."
            failed_rules.append(msg)
            checklist.append({
                "rule": "Academic Cutoff Percentage",
                "expected": f">= {job.min_percentage:.1f}%",
                "actual": f"{candidate.percentage:.1f}%",
                "passed": False,
                "details": msg
            })
        else:
            checklist.append({
                "rule": "Academic Cutoff Percentage",
                "expected": f">= {job.min_percentage:.1f}%",
                "actual": f"{candidate.percentage:.1f}%",
                "passed": True,
                "details": f"Candidate score {candidate.percentage:.1f}% meets cutoff {job.min_percentage:.1f}%."
            })

        # 6. Passing Year Check
        year_passed = True
        if job.min_passing_year and candidate.passing_year < job.min_passing_year:
            year_passed = False
        if job.max_passing_year and candidate.passing_year > job.max_passing_year:
            year_passed = False

        if not year_passed:
            msg = f"Passing year ({candidate.passing_year}) outside required bounds ({job.min_passing_year}-{job.max_passing_year})."
            failed_rules.append(msg)
            checklist.append({
                "rule": "Passing Year Bounds",
                "expected": f"{job.min_passing_year} - {job.max_passing_year}",
                "actual": str(candidate.passing_year),
                "passed": False,
                "details": msg
            })
        else:
            checklist.append({
                "rule": "Passing Year Bounds",
                "expected": f"{job.min_passing_year} - {job.max_passing_year}",
                "actual": str(candidate.passing_year),
                "passed": True,
                "details": f"Passing year {candidate.passing_year} is eligible."
            })

        # 7. Backlog Criteria
        if candidate.backlog_count > job.max_backlogs:
            msg = f"Active backlogs ({candidate.backlog_count}) exceeds allowed maximum of {job.max_backlogs}."
            failed_rules.append(msg)
            checklist.append({
                "rule": "Active Backlogs Criteria",
                "expected": f"<= {job.max_backlogs}",
                "actual": str(candidate.backlog_count),
                "passed": False,
                "details": msg
            })
        else:
            checklist.append({
                "rule": "Active Backlogs Criteria",
                "expected": f"<= {job.max_backlogs}",
                "actual": str(candidate.backlog_count),
                "passed": True,
                "details": f"Backlog count {candidate.backlog_count} is within allowed limit."
            })

        # 8. Technology Alignment
        tech_passed = True
        if job.required_technology:
            cand_tech = candidate.primary_technology.strip().lower()
            req_tech = job.required_technology.strip().lower()
            if cand_tech != req_tech and req_tech not in cand_tech:
                tech_passed = False
                msg = f"Candidate primary technology '{candidate.primary_technology}' does not match drive requirement '{job.required_technology}'."
                failed_rules.append(msg)
                checklist.append({
                    "rule": "Primary Technology Track",
                    "expected": job.required_technology,
                    "actual": candidate.primary_technology,
                    "passed": False,
                    "details": msg
                })
            else:
                checklist.append({
                    "rule": "Primary Technology Track",
                    "expected": job.required_technology,
                    "actual": candidate.primary_technology,
                    "passed": True,
                    "details": f"Technology '{candidate.primary_technology}' matches position."
                })

        # Compute Composite Eligibility
        passed_count = sum(1 for item in checklist if item["passed"])
        score = (passed_count / len(checklist)) * 100.0
        is_eligible = (len(failed_rules) == 0)

        if is_eligible:
            remarks = "Candidate meets all corporate eligibility requirements."
        else:
            remarks = "Candidate does not meet the eligibility criteria: " + "; ".join(failed_rules)

        if not is_eligible and raise_exception:
            raise IneligibleCandidateException(remarks, failed_rules=failed_rules)

        return EligibilityResult(
            is_eligible=is_eligible,
            score=round(score, 1),
            checklist=checklist,
            remarks=remarks
        )
