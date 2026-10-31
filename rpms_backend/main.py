"""
Recruitment & Placement Management System (RPMS)
Interactive Console CLI Application
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
from rpms_backend.dao import CandidateDAO, JobDAO, CompanyDAO, ApplicationDAO, InterviewDAO, PlacementDAO
from rpms_backend.utils import ReportExporter
from rpms_backend.exceptions import RPMSException

def clear_screen():
    print("\n" * 2)

def print_header():
    print("=" * 76)
    print("      KIRAN ACADEMY - RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM")
    print("               Enterprise Business Console Application")
    print("=" * 76)

def main_menu():
    print_header()
    print("""
  [1] Candidate Directory (Register, Search, Browse)
  [2] Corporate Employers (Register, View Partners)
  [3] Job Openings & Drives (Post Requirement, View Openings)
  [4] Application Processing & Automated Eligibility Engine
  [5] Interview Round Coordination & Panel Feedback
  [6] Selection, Offer Issuance & Final Placement
  [7] Management Relational Reports & File Export (CSV/TXT)
  [8] Run Complete Automated System Lifecycle Demo
  [0] Exit Portal
    """)
    choice = input("Enter choice [0-8]: ").strip()
    return choice

def candidate_menu(cand_dao: CandidateDAO, service: RecruitmentService):
    while True:
        print("\n--- CANDIDATE MANAGEMENT ---")
        print("1. View All Candidates")
        print("2. Search Candidates by Technology (Java/Python/Testing/Analytics)")
        print("3. Register New Candidate Profile")
        print("0. Back to Main Menu")
        c = input("Choice: ").strip()

        if c == "1":
            cands = cand_dao.get_all()
            print(f"\nTotal Candidates: {len(cands)}")
            print(f"{'Code':<15} {'Full Name':<20} {'Qual':<8} {'Percentage':<10} {'Track':<15} {'Status':<12}")
            print("-" * 80)
            for cand in cands:
                print(f"{cand.candidate_code:<15} {cand.full_name:<20} {cand.qualification:<8} {cand.percentage:<10.1f} {cand.primary_technology:<15} {cand.placement_status:<12}")
        elif c == "2":
            tech = input("Enter Technology (e.g. Java, Python): ").strip()
            cands = cand_dao.get_all(technology=tech)
            print(f"\nCandidates in track '{tech}': {len(cands)}")
            for cand in cands:
                print(f"  {cand.candidate_code} | {cand.full_name} | {cand.college} | {cand.percentage}% | Status: {cand.placement_status}")
        elif c == "3":
            print("\nEnter New Candidate Details:")
            name = input("Full Name: ").strip()
            email = input("Email Address: ").strip()
            mobile = input("Mobile Number (10 digits): ").strip()
            qual = input("Qualification (BE/BTech/MCA/BCA): ").strip() or "BE"
            college = input("College Name: ").strip() or "Pune College"
            pct = float(input("Aggregate Percentage (0-100): ").strip() or "70.0")
            backlogs = int(input("Backlog Count: ").strip() or "0")
            tech = input("Primary Technology (Java/Python/Testing): ").strip() or "Java"

            cand = Candidate(
                full_name=name, email=email, mobile=mobile,
                qualification=qual, college=college, percentage=pct,
                backlog_count=backlogs, primary_technology=tech
            )
            try:
                saved = service.register_candidate(cand)
                print(f"✓ Registered Candidate: {saved.full_name} (Code: {saved.candidate_code})")
            except Exception as e:
                print(f"✗ Validation/Save Error: {e}")
        elif c == "0":
            break

def eligibility_menu(engine: CandidateEligibilityEngine, service: RecruitmentService, cand_dao: CandidateDAO, job_dao: JobDAO):
    print("\n--- CANDIDATE ELIGIBILITY ENGINE WORKBENCH ---")
    cands = cand_dao.get_all()
    jobs = job_dao.get_all()

    print("\nAvailable Candidates:")
    for cand in cands[:5]:
        print(f"  ID {cand.candidate_id}: {cand.full_name} ({cand.qualification}, {cand.percentage}%, {cand.backlog_count} backlogs, {cand.primary_technology})")

    print("\nAvailable Job Drives:")
    for job in jobs[:5]:
        print(f"  ID {job.job_id}: {job.job_title} ({job.job_code}) - Min {job.min_percentage}%, Max {job.max_backlogs} backlogs, {job.required_technology}")

    try:
        c_id = int(input("\nEnter Candidate ID to evaluate: ").strip() or "1")
        j_id = int(input("Enter Job ID to evaluate: ").strip() or "1")

        cand = cand_dao.get_by_id(c_id)
        job = job_dao.get_by_id(j_id)

        if not cand or not job:
            print("Invalid Candidate or Job ID.")
            return

        print(f"\nRunning Automated Rule Evaluation: '{cand.full_name}' -> '{job.job_title}'...")
        res = engine.evaluate(cand, job)
        print(f"Verdict     : {'✓ ELIGIBLE FOR APPLICATION' if res.is_eligible else '✗ INELIGIBLE'}")
        print(f"Score       : {res.score}/100.0")
        print(f"Diagnostics : {res.remarks}")
        print("\nChecklist Breakdown:")
        for chk in res.checklist:
            icon = "✓" if chk["passed"] else "✗"
            print(f"  [{icon}] {chk['rule']:<28} | Expected: {chk['expected']:<20} | Actual: {chk['actual']:<15}")

        if res.is_eligible:
            apply_now = input("\nSubmit Application for this candidate? (y/n): ").strip().lower()
            if apply_now == "y":
                try:
                    app = service.apply_for_job(c_id, j_id)
                    print(f"✓ Application created: {app.application_code}")
                except Exception as ex:
                    print(f"✗ Could not submit: {ex}")
    except ValueError:
        print("Invalid numerical input.")

def reports_menu(report_service: ReportService):
    print("\n--- MANAGEMENT RELATIONAL REPORTS & AUDIT ---")
    print("1. Recruitment Conversion Funnel Summary")
    print("2. Company-wise Placement Share & Average CTC")
    print("3. Technology Specialization Distribution")
    print("4. Active Openings Aging Monitor")
    print("5. Export All Reports to Files (CSV & Text)")
    choice = input("Choice: ").strip()

    if choice == "1":
        funnel = report_service.get_funnel_statistics()
        print("\nRecruitment Funnel Conversion Rates:")
        for k, v in funnel.items():
            print(f"  {k.replace('_', ' ').title():<30}: {v}")
    elif choice == "2":
        comps = report_service.get_company_wise_placement_report()
        print(f"\n{'Company Name':<30} {'Industry':<20} {'Placed':<8} {'Avg CTC':<10} {'Highest':<10}")
        print("-" * 80)
        for c in comps:
            print(f"{c['company_name']:<30} {c['industry']:<20} {c['total_placed']:<8} {c['avg_package']:.2f} LPA   {c['highest_package']:.2f} LPA")
    elif choice == "3":
        techs = report_service.get_technology_wise_placement_report()
        print(f"\n{'Technology':<25} {'Total Placed':<12} {'Avg CTC':<10} {'Max CTC':<10}")
        print("-" * 60)
        for t in techs:
            print(f"{t['technology']:<25} {t['total_placed']:<12} {t['avg_package']:.2f} LPA   {t['max_package']:.2f} LPA")
    elif choice == "4":
        aging = report_service.get_open_jobs_aging_report()
        print(f"\n{'Job Code':<15} {'Position':<30} {'Company':<20} {'Openings':<10} {'Applicants':<10}")
        print("-" * 85)
        for a in aging:
            print(f"{a['job_code']:<15} {a['job_title']:<30} {a['company_name']:<20} {a['openings']:<10} {a['total_applicants']:<10}")
    elif choice == "5":
        funnel = report_service.get_funnel_statistics()
        comps = report_service.get_company_wise_placement_report()
        techs = report_service.get_technology_wise_placement_report()
        txt_path = ReportExporter.export_summary_text(funnel, comps, techs)
        print(f"✓ Summary report exported to: {txt_path}")

def run_cli():
    service = RecruitmentService()
    eligibility_engine = CandidateEligibilityEngine()
    report_service = ReportService()
    cand_dao = CandidateDAO()
    job_dao = JobDAO()

    while True:
        ch = main_menu()
        if ch == "1":
            candidate_menu(cand_dao, service)
        elif ch == "2":
            comps = CompanyDAO().get_all()
            print(f"\n{'Code':<12} {'Company Name':<30} {'Industry':<20} {'Status':<10}")
            print("-" * 75)
            for cp in comps:
                print(f"{cp.company_code:<12} {cp.company_name:<30} {cp.industry:<20} {cp.status:<10}")
        elif ch == "3":
            jobs = job_dao.get_all()
            print(f"\n{'Job Code':<15} {'Title':<32} {'Package':<15} {'Status':<10}")
            print("-" * 75)
            for j in jobs:
                print(f"{j.job_code:<15} {j.job_title:<32} {j.min_package:.1f}-{j.max_package:.1f} LPA     {j.status:<10}")
        elif ch == "4":
            eligibility_menu(eligibility_engine, service, cand_dao, job_dao)
        elif ch == "5":
            rounds = InterviewDAO().get_all()
            print(f"\n{'Code':<15} {'Round':<20} {'Date':<15} {'Interviewer':<20} {'Status':<12}")
            print("-" * 82)
            for r in rounds:
                print(f"{r.interview_code:<15} {r.round_name:<20} {r.scheduled_date:<15} {r.interviewer_name:<20} {r.status:<12}")
        elif ch == "6":
            offers = PlacementDAO().get_all_offers()
            print(f"\n{'Offer Code':<15} {'Role':<28} {'Package':<10} {'Status':<12}")
            print("-" * 65)
            for o in offers:
                print(f"{o.offer_code:<15} {o.offered_role:<28} {o.offered_package:<10.1f} {o.status:<12}")
        elif ch == "7":
            reports_menu(report_service)
        elif ch == "8":
            from rpms_backend.run_demo import run_demonstration
            run_demonstration()
        elif ch == "0":
            print("\nExiting Kiran Academy RPMS Enterprise Portal. Goodbye!")
            break
        else:
            print("Invalid choice, please select 0-8.")

if __name__ == "__main__":
    run_cli()
