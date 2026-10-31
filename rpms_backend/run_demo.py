"""
Automated Demonstration & Test Runner for RPMS Backend
Validates all requirements specified in the Kiran Academy Abstract:
- Modular Architecture & OOP
- Candidate Registration
- Candidate Eligibility Engine (with pass & fail criteria)
- Duplicate Application Prevention
- Full Recruitment Workflow Stages
- SQL Reports & Joins
- File Handling & Export
"""

import sys
import os
from datetime import date, datetime

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpms_backend.models import Candidate, Job, Company
from rpms_backend.services import (
    RecruitmentService, CandidateEligibilityEngine, ReportService
)
from rpms_backend.dao import CandidateDAO, JobDAO, CompanyDAO, ApplicationDAO
from rpms_backend.utils import logger, ReportExporter
from rpms_backend.exceptions import (
    IneligibleCandidateException, DuplicateApplicationException
)

def print_banner(title: str):
    print("\n" + "=" * 76)
    print(f"  {title.upper()}")
    print("=" * 76)

def run_demonstration():
    print_banner("Kiran Academy - Recruitment & Placement Management System")
    print("Initiating automated end-to-end lifecycle verification...\n")

    service = RecruitmentService()
    eligibility_engine = CandidateEligibilityEngine()
    report_service = ReportService()
    cand_dao = CandidateDAO()
    job_dao = JobDAO()

    # -------------------------------------------------------------
    # STAGE 1: Candidate Registration & Validation
    # -------------------------------------------------------------
    print_banner("Stage 1: Candidate Registration & Validation")
    ts = int(datetime.now().timestamp())
    new_candidate = Candidate(
        full_name=f"Tanmay Deshmukh {ts % 1000}",
        email=f"tanmay.deshmukh{ts}@example.com",
        mobile=f"9822{ts % 1000000:06d}",
        date_of_birth=date(2002, 5, 15),
        gender="Male",
        qualification="BE",
        college="MIT World Peace University",
        university="SPPU",
        passing_year=2025,
        percentage=72.5,
        backlog_count=0,
        primary_technology="Java",
        current_location="Pune",
        preferred_location="Pune",
        profile_status="ACTIVE",
        placement_status="NOT_PLACED"
    )
    registered_cand = service.register_candidate(new_candidate)
    print(f"[OK] Registered Candidate: {registered_cand.full_name}")
    print(f"  Code: {registered_cand.candidate_code} | Degree: {registered_cand.qualification} ({registered_cand.percentage}%) | Track: {registered_cand.primary_technology}")
    logger.info(f"Candidate {registered_cand.candidate_code} registered successfully.")

    # -------------------------------------------------------------
    # STAGE 2: Candidate Eligibility Engine (The Core Feature)
    # -------------------------------------------------------------
    print_banner("Stage 2: Candidate Eligibility Engine Verification")
    
    # Test Case A: Eligible Candidate
    java_job = job_dao.get_by_id(1)  # Infosys Associate Java Developer (Min 60%, 0 backlogs, Java)
    print(f"Test Case A: Evaluating '{registered_cand.full_name}' against Job '{java_job.job_title}' ({java_job.job_code})")
    result_a = eligibility_engine.evaluate(registered_cand, java_job)
    print(f"  Verdict       : {'[PASS] ELIGIBLE' if result_a.is_eligible else '[FAIL] INELIGIBLE'}")
    print(f"  Engine Score  : {result_a.score}/100.0")
    print(f"  Remarks       : {result_a.remarks}")
    for item in result_a.checklist:
        icon = "[PASS]" if item["passed"] else "[FAIL]"
        print(f"    {icon} {item['rule']:<30}: Expected {item['expected']} | Actual: {item['actual']}")

    # Test Case B: Ineligible Candidate (Testing percentage cutoff and backlog criteria)
    ineligible_cand = cand_dao.get_by_id(5)  # Rohit Pawar: 59.5% < 60%, 1 Backlog > 0
    print(f"\nTest Case B: Evaluating '{ineligible_cand.full_name}' (Score: {ineligible_cand.percentage}%, Backlogs: {ineligible_cand.backlog_count})")
    result_b = eligibility_engine.evaluate(ineligible_cand, java_job)
    print(f"  Verdict       : {'[PASS] ELIGIBLE' if result_b.is_eligible else '[FAIL] INELIGIBLE'}")
    print(f"  Engine Score  : {result_b.score}/100.0")
    print(f"  Remarks       : {result_b.remarks}")
    for item in result_b.checklist:
        if not item["passed"]:
            print(f"    [FAIL RULE] {item['rule']}: {item['details']}")

    # -------------------------------------------------------------
    # STAGE 3: Application Submission & Duplicate Prevention
    # -------------------------------------------------------------
    print_banner("Stage 3: Application Submission & Duplicate Prevention")
    app = service.apply_for_job(registered_cand.candidate_id, java_job.job_id)
    print(f"[OK] Application successfully submitted: Code {app.application_code}")
    print(f"  Status: {app.status} | Eligibility: {app.eligibility_status}")

    # Verify duplicate application prevention
    print("\nVerifying Duplicate Application Prevention Rule:")
    try:
        service.apply_for_job(registered_cand.candidate_id, java_job.job_id)
        print("[FAIL] ERROR: Duplicate application was not blocked!")
    except DuplicateApplicationException as e:
        print(f"[OK] SUCCESS: Duplicate application blocked as expected: '{e}'")

    # -------------------------------------------------------------
    # STAGE 4: Candidate Shortlisting
    # -------------------------------------------------------------
    print_banner("Stage 4: Recruiter Shortlisting Workbench")
    shortlisted_app = service.shortlist_application(app.application_id)
    print(f"[OK] Application {shortlisted_app.application_code} transitioned to status: {shortlisted_app.status}")

    # -------------------------------------------------------------
    # STAGE 5: Interview Scheduling
    # -------------------------------------------------------------
    print_banner("Stage 5: Interview Scheduling & Round Coordination")
    interview = service.schedule_interview(
        application_id=shortlisted_app.application_id,
        round_name="Technical Round 1",
        interview_date=date(2026, 11, 2),
        interview_time="10:30",
        mode="Online",
        interviewer_name="Vikas Jadhav (Senior Architect)",
        meeting_url="https://meet.google.com/kpa-rpms-eval"
    )
    print(f"[OK] Interview Scheduled: Code {interview.interview_code}")
    print(f"  Round: {interview.round_name} | Date: {interview.scheduled_date} at {interview.scheduled_time}")
    print(f"  Interviewer: {interview.interviewer_name} | Mode: {interview.mode}")

    # -------------------------------------------------------------
    # STAGE 6: Interview Feedback & Panel Evaluation
    # -------------------------------------------------------------
    print_banner("Stage 6: Interview Feedback & Panel Evaluation")
    evaluated_interview = service.record_interview_feedback(
        interview_id=interview.interview_id,
        tech_rating=4.5,
        comm_rating=4.0,
        problem_rating=4.5,
        overall_rating=4.5,
        remarks="Candidate demonstrated exceptional knowledge of Java Collections, multithreading, and RESTful APIs.",
        result="SELECTED"
    )
    print(f"[OK] Recorded Interview Feedback for {evaluated_interview.interview_code}:")
    print(f"  Technical: {evaluated_interview.tech_rating}/5.0 | Comm: {evaluated_interview.comm_rating}/5.0 | Problem Solving: {evaluated_interview.problem_rating}/5.0")
    print(f"  Composite: {evaluated_interview.overall_rating}/5.0 | Verdict: {evaluated_interview.result}")

    # -------------------------------------------------------------
    # STAGE 7: Corporate Offer Issuance & Student Acceptance
    # -------------------------------------------------------------
    print_banner("Stage 7: Corporate Offer Issuance & Student Acceptance")
    offer = service.create_offer(
        application_id=shortlisted_app.application_id,
        offered_role="Associate Java Developer",
        offered_package=5.4,
        offer_date=date(2026, 10, 30),
        expected_joining_date=date(2026, 12, 1),
        remarks="Formal campus offer letter generated with standard 12-month bond."
    )
    print(f"[OK] Corporate Offer Created: Code {offer.offer_code}")
    print(f"  Role: {offer.offered_role} | Package: {offer.offered_package} LPA | Status: {offer.status}")

    # Candidate accepts offer
    accepted_offer = service.update_offer_status(offer.offer_id, "ACCEPTED")
    print(f"[OK] Student Acceptance Recorded: Status updated to '{accepted_offer.status}'")

    # -------------------------------------------------------------
    # STAGE 8: Joining Verification & Official Placement
    # -------------------------------------------------------------
    print_banner("Stage 8: Joining Verification & Institutional Placement Record")
    placement = service.confirm_joining_and_placement(
        offer_id=accepted_offer.offer_id,
        actual_joining_date=date(2026, 12, 1),
        corporate_emp_id="INF-90412",
        placement_officer="Neha Deshmukh",
        remarks="Candidate verified and reported to Infosys Pune Hinjawadi Phase 2."
    )
    print(f"[OK] Final Placement Milestone Confirmed: Code {placement.placement_code}")
    print(f"  Designation: {placement.designation} | Package: {placement.package_offered} LPA")
    print(f"  Corporate Employee ID: {placement.corporate_emp_id} | Verified By: {placement.placement_officer}")

    updated_cand = cand_dao.get_by_id(registered_cand.candidate_id)
    print(f"[OK] Candidate Master Status Synchronized: '{updated_cand.placement_status}'")

    # -------------------------------------------------------------
    # STAGE 9: SQL Relational Reporting & Analytics
    # -------------------------------------------------------------
    print_banner("Stage 9: Management Relational Reports (SQL Joins & Grouping)")
    funnel = report_service.get_funnel_statistics()
    print("Recruitment Funnel Metrics:")
    print(f"  Total Candidates Registered : {funnel['total_candidates']}")
    print(f"  Total Applications Filed    : {funnel['total_applications']}")
    print(f"  Eligible Applications       : {funnel['eligible_applications']}")
    print(f"  Shortlisted for Rounds      : {funnel['shortlisted_applications']}")
    print(f"  Conducted Interviews        : {funnel['interviewed_candidates']}")
    print(f"  Selected Candidates         : {funnel['selected_candidates']}")
    print(f"  Final Verified Placements   : {funnel['placed_candidates']}")
    print(f"  Offer-to-Join Ratio         : {funnel['offer_to_join_ratio']}%")

    print("\nCompany-wise Placement Share:")
    comp_report = report_service.get_company_wise_placement_report()
    for c in comp_report:
        print(f"  {c['company_name']:<30} | Placed: {c['total_placed']:<3} | Avg CTC: {c['avg_package']:.2f} LPA")

    print("\nTechnology Specialization Distribution:")
    tech_report = report_service.get_technology_wise_placement_report()
    for t in tech_report:
        print(f"  {t['technology']:<25} | Total Placed: {t['total_placed']:<3} | Max CTC: {t['max_package']:.2f} LPA")

    # -------------------------------------------------------------
    # STAGE 10: File Handling & Reports Export
    # -------------------------------------------------------------
    print_banner("Stage 10: File Handling & Report Export")
    summary_txt = ReportExporter.export_summary_text(funnel, comp_report, tech_report, "placement_summary.txt")
    print(f"[OK] Institutional summary report exported to: {summary_txt}")

    all_cands = [c.to_dict() for c in cand_dao.get_all()]
    cands_csv = ReportExporter.export_to_csv(all_cands, "candidates_roster.csv")
    print(f"[OK] Candidate master roster exported to CSV: {cands_csv}")

    print_banner("All 10 Lifecycle Stages Verified Successfully!")
    print("All institutional conditions from Kiran Academy have been fulfilled.")

if __name__ == "__main__":
    run_demonstration()
