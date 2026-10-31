"""
Job Requirement Data Access Object (DAO)
Performs database operations for campus recruitment job postings
"""

from typing import List, Optional
from rpms_backend.database import DatabaseManager
from rpms_backend.models import Job

class JobDAO:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def save(self, job: Job) -> Job:
        job.validate()
        cursor = self.db.cursor()

        quals_str = ",".join(job.allowed_qualifications) if isinstance(job.allowed_qualifications, list) else str(job.allowed_qualifications)
        skills_str = ",".join(job.required_skills) if isinstance(job.required_skills, list) else str(job.required_skills)

        if job.job_id:
            query = """
            UPDATE jobs SET
                company_id = ?, job_title = ?, openings = ?, employment_type = ?,
                location = ?, min_package = ?, max_package = ?, allowed_qualifications = ?,
                min_percentage = ?, min_passing_year = ?, max_passing_year = ?,
                max_backlogs = ?, required_technology = ?, required_skills = ?,
                posted_date = ?, deadline_date = ?, status = ?
            WHERE job_id = ?
            """
            cursor.execute(query, (
                job.company_id, job.job_title, job.openings, job.employment_type,
                job.location, job.min_package, job.max_package, quals_str,
                job.min_percentage, job.min_passing_year, job.max_passing_year,
                job.max_backlogs, job.required_technology, skills_str,
                str(job.posted_date) if job.posted_date else None,
                str(job.deadline_date) if job.deadline_date else None,
                job.status, job.job_id
            ))
        else:
            if not job.job_code:
                cursor.execute("SELECT COUNT(*) FROM jobs")
                count = cursor.fetchone()[0] + 1
                job.job_code = f"JOB-2026-{count:03d}"

            query = """
            INSERT INTO jobs (
                job_code, company_id, job_title, openings, employment_type,
                location, min_package, max_package, allowed_qualifications,
                min_percentage, min_passing_year, max_passing_year, max_backlogs,
                required_technology, required_skills, posted_date, deadline_date,
                status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                job.job_code, job.company_id, job.job_title, job.openings, job.employment_type,
                job.location, job.min_package, job.max_package, quals_str,
                job.min_percentage, job.min_passing_year, job.max_passing_year, job.max_backlogs,
                job.required_technology, skills_str,
                str(job.posted_date) if job.posted_date else None,
                str(job.deadline_date) if job.deadline_date else None,
                job.status
            ))
            job.job_id = cursor.lastrowid

        self.db.commit()
        return job

    def get_by_id(self, job_id: int) -> Optional[Job]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        row = cursor.fetchone()
        return self._row_to_job(row) if row else None

    def get_by_code(self, job_code: str) -> Optional[Job]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM jobs WHERE job_code = ?", (job_code,))
        row = cursor.fetchone()
        return self._row_to_job(row) if row else None

    def get_all(self, status: str = None, technology: str = None) -> List[Job]:
        cursor = self.db.cursor()
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if technology:
            query += " AND required_technology = ?"
            params.append(technology)
        query += " ORDER BY job_id ASC"
        cursor.execute(query, params)
        return [self._row_to_job(row) for row in cursor.fetchall()]

    def update_status(self, job_id: int, status: str):
        cursor = self.db.cursor()
        cursor.execute("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
        self.db.commit()

    def _row_to_job(self, row) -> Job:
        quals = [q.strip() for q in row["allowed_qualifications"].split(",") if q.strip()]
        skills = [s.strip() for s in (row["required_skills"] or "").split(",") if s.strip()]
        return Job(
            job_id=row["job_id"],
            job_code=row["job_code"],
            company_id=row["company_id"],
            job_title=row["job_title"],
            openings=row["openings"],
            employment_type=row["employment_type"] or "Full-time",
            location=row["location"],
            min_package=float(row["min_package"] or 0),
            max_package=float(row["max_package"] or 0),
            allowed_qualifications=quals,
            min_percentage=float(row["min_percentage"] or 0),
            min_passing_year=row["min_passing_year"],
            max_passing_year=row["max_passing_year"],
            max_backlogs=int(row["max_backlogs"] or 0),
            required_technology=row["required_technology"],
            required_skills=skills,
            posted_date=row["posted_date"],
            deadline_date=row["deadline_date"],
            status=row["status"],
        )
