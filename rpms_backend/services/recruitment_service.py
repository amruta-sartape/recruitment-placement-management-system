"""
Recruitment Lifecycle Service
Orchestrates end-to-end recruitment workflow from registration to placement
"""

from typing import Optional
from datetime import datetime, date
from rpms_backend.models import (
    Candidate, Job, Application, InterviewRound, Offer, Placement
)
from rpms_backend.dao import (
    CandidateDAO, CompanyDAO, JobDAO, ApplicationDAO,
    InterviewDAO, PlacementDAO
)
from rpms_backend.services.eligibility_engine import CandidateEligibilityEngine
from rpms_backend.exceptions import (
    CandidateNotFoundException,
    JobNotFoundException,
    ValidationException,
    InvalidProcessStateException
)

class RecruitmentService:
    def __init__(self):
        self.candidate_dao = CandidateDAO()
        self.company_dao = CompanyDAO()
        self.job_dao = JobDAO()
        self.app_dao = ApplicationDAO()
        self.interview_dao = InterviewDAO()
        self.placement_dao = PlacementDAO()
        self.eligibility_engine = CandidateEligibilityEngine()

    # Stage 1: Candidate Registration
    def register_candidate(self, candidate: Candidate) -> Candidate:
        candidate.validate()
        existing = self.candidate_dao.get_by_email(candidate.email)
        if existing and existing.candidate_id != candidate.candidate_id:
            raise ValidationException(f"Candidate with email {candidate.email} already exists.")
        return self.candidate_dao.save(candidate)

    # Stage 2: Eligibility Verification
    def verify_eligibility(self, candidate_id: int, job_id: int):
        candidate = self.candidate_dao.get_by_id(candidate_id)
        if not candidate:
            raise CandidateNotFoundException(f"Candidate ID {candidate_id} not found.")

        job = self.job_dao.get_by_id(job_id)
        if not job:
            raise JobNotFoundException(f"Job ID {job_id} not found.")

        return self.eligibility_engine.evaluate(candidate, job, raise_exception=False)

    # Stage 3: Job Application
    def apply_for_job(self, candidate_id: int, job_id: int) -> Application:
        candidate = self.candidate_dao.get_by_id(candidate_id)
        if not candidate:
            raise CandidateNotFoundException(f"Candidate ID {candidate_id} not found.")

        job = self.job_dao.get_by_id(job_id)
        if not job:
            raise JobNotFoundException(f"Job ID {job_id} not found.")

        # Evaluate through Eligibility Engine (strictly raises exception on failure)
        elig_result = self.eligibility_engine.evaluate(candidate, job, raise_exception=True)

        app = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            applied_at=datetime.now(),
            status="APPLIED" if elig_result.is_eligible else "REJECTED",
            eligibility_status="ELIGIBLE" if elig_result.is_eligible else "INELIGIBLE",
            eligibility_remarks=elig_result.remarks
        )
        return self.app_dao.save(app)

    # Stage 4: Candidate Shortlisting
    def shortlist_application(self, application_id: int) -> Application:
        app = self.app_dao.get_by_id(application_id)
        if not app:
            raise ValidationException(f"Application ID {application_id} not found.")

        if app.eligibility_status != "ELIGIBLE":
            raise InvalidProcessStateException("Cannot shortlist an ineligible candidate.")

        app.status = "SHORTLISTED"
        return self.app_dao.save(app)

    # Stage 5: Interview Scheduling
    def schedule_interview(self, application_id: int, round_name: str,
                           interview_date, interview_time, mode="Online",
                           interviewer_name="", meeting_url="") -> InterviewRound:
        app = self.app_dao.get_by_id(application_id)
        if not app:
            raise ValidationException(f"Application ID {application_id} not found.")

        interview = InterviewRound(
            application_id=application_id,
            round_name=round_name,
            scheduled_date=interview_date,
            scheduled_time=interview_time,
            mode=mode,
            interviewer_name=interviewer_name,
            meeting_url=meeting_url,
            status="SCHEDULED"
        )
        saved_interview = self.interview_dao.save(interview)
        app.status = "INTERVIEW_SCHEDULED"
        self.app_dao.save(app)
        return saved_interview

    # Stage 6: Interview Feedback & Evaluation
    def record_interview_feedback(self, interview_id: int, tech_rating: float,
                                  comm_rating: float, problem_rating: float,
                                  overall_rating: float, remarks: str, result: str) -> InterviewRound:
        interview = self.interview_dao.get_by_id(interview_id)
        if not interview:
            raise ValidationException(f"Interview ID {interview_id} not found.")

        interview.tech_rating = tech_rating
        interview.comm_rating = comm_rating
        interview.problem_rating = problem_rating
        interview.overall_rating = overall_rating
        interview.feedback_remarks = remarks
        interview.result = result
        interview.status = "COMPLETED"

        self.interview_dao.save(interview)

        # Update application status if round decided
        app = self.app_dao.get_by_id(interview.application_id)
        if app:
            if result == "SELECTED":
                app.status = "SELECTED"
            elif result == "REJECTED":
                app.status = "REJECTED"
            self.app_dao.save(app)

        return interview

    # Stage 7 & 8: Selection & Corporate Offer Issuance
    def create_offer(self, application_id: int, offered_role: str,
                     offered_package: float, offer_date: date,
                     expected_joining_date: date, remarks: str = "") -> Offer:
        app = self.app_dao.get_by_id(application_id)
        if not app:
            raise ValidationException(f"Application ID {application_id} not found.")

        job = self.job_dao.get_by_id(app.job_id)
        candidate = self.candidate_dao.get_by_id(app.candidate_id)

        offer = Offer(
            application_id=application_id,
            candidate_id=candidate.candidate_id,
            company_id=job.company_id,
            job_id=job.job_id,
            offered_role=offered_role,
            offered_package=offered_package,
            offer_date=offer_date,
            expected_joining_date=expected_joining_date,
            status="OFFERED",
            remarks=remarks
        )
        return self.placement_dao.save_offer(offer)

    def update_offer_status(self, offer_id: int, status: str) -> Offer:
        offer = self.placement_dao.get_offer_by_id(offer_id)
        if not offer:
            raise ValidationException(f"Offer ID {offer_id} not found.")
        offer.status = status
        return self.placement_dao.save_offer(offer)

    # Stage 9 & 10: Joining Verification & Official Placement
    def confirm_joining_and_placement(self, offer_id: int, actual_joining_date: date,
                                      corporate_emp_id: str, placement_officer="Neha Deshmukh",
                                      remarks="") -> Placement:
        offer = self.placement_dao.get_offer_by_id(offer_id)
        if not offer:
            raise ValidationException(f"Offer ID {offer_id} not found.")

        placement = Placement(
            offer_id=offer_id,
            candidate_id=offer.candidate_id,
            company_id=offer.company_id,
            job_id=offer.job_id,
            designation=offer.offered_role,
            package_offered=offer.offered_package,
            actual_joining_date=actual_joining_date,
            joining_status="JOINED",
            corporate_emp_id=corporate_emp_id,
            placement_officer=placement_officer,
            remarks=remarks
        )
        saved_placement = self.placement_dao.save_placement(placement)

        # Update candidate master placement status to PLACED
        self.candidate_dao.update_placement_status(offer.candidate_id, "PLACED")

        # Update offer status to ACCEPTED/JOINED
        offer.status = "ACCEPTED"
        self.placement_dao.save_offer(offer)

        return saved_placement
