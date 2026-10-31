"""
Report and Analytics Service
Generates SQL relational reports using joins, groupings, and aggregations
"""

from typing import List, Dict, Any
from rpms_backend.database import DatabaseManager

class ReportService:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def get_funnel_statistics(self) -> Dict[str, Any]:
        """Calculates recruitment funnel transition counts and rates"""
        cursor = self.db.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM candidates")
        total_candidates = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications")
        total_apps = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE eligibility_status = 'ELIGIBLE'")
        eligible_apps = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE status IN ('SHORTLISTED', 'INTERVIEW_SCHEDULED', 'SELECTED')")
        shortlisted = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT application_id) FROM interview_rounds")
        interviewed = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'SELECTED'")
        selected = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM placements WHERE joining_status = 'JOINED'")
        placed = cursor.fetchone()[0]

        offer_to_join_rate = round((placed / selected * 100.0), 1) if selected > 0 else 0.0

        return {
            "total_candidates": total_candidates,
            "total_applications": total_apps,
            "eligible_applications": eligible_apps,
            "shortlisted_applications": shortlisted,
            "interviewed_candidates": interviewed,
            "selected_candidates": selected,
            "placed_candidates": placed,
            "offer_to_join_ratio": offer_to_join_rate
        }

    def get_company_wise_placement_report(self) -> List[Dict[str, Any]]:
        """Company-wise placement volume, average package, and highest offer (JOIN query)"""
        cursor = self.db.cursor()
        query = """
        SELECT
            c.company_code,
            c.company_name,
            c.industry,
            COUNT(p.placement_id) AS total_placed,
            ROUND(AVG(p.package_offered), 2) AS avg_package,
            MAX(p.package_offered) AS highest_package
        FROM companies c
        LEFT JOIN placements p ON c.company_id = p.company_id AND p.joining_status = 'JOINED'
        GROUP BY c.company_id, c.company_code, c.company_name, c.industry
        ORDER BY total_placed DESC, avg_package DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        report = []
        for r in rows:
            report.append({
                "company_code": r[0],
                "company_name": r[1],
                "industry": r[2],
                "total_placed": r[3] or 0,
                "avg_package": r[4] or 0.0,
                "highest_package": r[5] or 0.0,
            })
        return report

    def get_technology_wise_placement_report(self) -> List[Dict[str, Any]]:
        """Technology track placement counts and package distribution (JOIN query)"""
        cursor = self.db.cursor()
        query = """
        SELECT
            cand.primary_technology,
            COUNT(p.placement_id) AS total_placed,
            ROUND(AVG(p.package_offered), 2) AS avg_package,
            MAX(p.package_offered) AS max_package
        FROM candidates cand
        JOIN placements p ON cand.candidate_id = p.candidate_id
        WHERE p.joining_status = 'JOINED'
        GROUP BY cand.primary_technology
        ORDER BY total_placed DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        report = []
        for r in rows:
            report.append({
                "technology": r[0],
                "total_placed": r[1] or 0,
                "avg_package": r[2] or 0.0,
                "max_package": r[3] or 0.0,
            })
        return report

    def get_open_jobs_aging_report(self) -> List[Dict[str, Any]]:
        """Active jobs and vacancy availability (JOIN query)"""
        cursor = self.db.cursor()
        query = """
        SELECT
            j.job_code,
            j.job_title,
            c.company_name,
            j.openings,
            j.min_package,
            j.max_package,
            j.posted_date,
            j.deadline_date,
            COUNT(a.application_id) AS total_applicants
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN applications a ON j.job_id = a.job_id
        WHERE j.status = 'OPEN'
        GROUP BY j.job_id, j.job_code, j.job_title, c.company_name
        ORDER BY j.deadline_date ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        report = []
        for r in rows:
            report.append({
                "job_code": r[0],
                "job_title": r[1],
                "company_name": r[2],
                "openings": r[3],
                "package_range": f"{r[4]:.1f} - {r[5]:.1f} LPA",
                "posted_date": r[6],
                "deadline_date": r[7],
                "total_applicants": r[8] or 0,
            })
        return report
