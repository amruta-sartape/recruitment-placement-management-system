"""
Application Data Access Object (DAO)
Performs database operations for candidate job applications
"""

from typing import List, Optional
from datetime import datetime
from rpms_backend.database import DatabaseManager
from rpms_backend.models import Application

class ApplicationDAO:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def save(self, application: Application) -> Application:
        cursor = self.db.cursor()

        if application.application_id:
            query = """
            UPDATE applications SET
                status = ?, eligibility_status = ?, eligibility_remarks = ?
            WHERE application_id = ?
            """
            cursor.execute(query, (
                application.status, application.eligibility_status,
                application.eligibility_remarks, application.application_id
            ))
        else:
            if not application.application_code:
                cursor.execute("SELECT COUNT(*) FROM applications")
                count = cursor.fetchone()[0] + 1
                application.application_code = f"APP-2026-{count:04d}"

            if not application.applied_at:
                application.applied_at = datetime.now()

            query = """
            INSERT INTO applications (
                application_code, candidate_id, job_id, applied_at, status,
                eligibility_status, eligibility_remarks
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                application.application_code, application.candidate_id,
                application.job_id, str(application.applied_at),
                application.status, application.eligibility_status,
                application.eligibility_remarks
            ))
            application.application_id = cursor.lastrowid

        self.db.commit()
        return application

    def get_by_id(self, application_id: int) -> Optional[Application]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM applications WHERE application_id = ?", (application_id,))
        row = cursor.fetchone()
        return self._row_to_app(row) if row else None

    def get_by_candidate_and_job(self, candidate_id: int, job_id: int) -> Optional[Application]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM applications WHERE candidate_id = ? AND job_id = ?", (candidate_id, job_id))
        row = cursor.fetchone()
        return self._row_to_app(row) if row else None

    def get_all(self, job_id: int = None, candidate_id: int = None, status: str = None) -> List[Application]:
        cursor = self.db.cursor()
        query = "SELECT * FROM applications WHERE 1=1"
        params = []
        if job_id:
            query += " AND job_id = ?"
            params.append(job_id)
        if candidate_id:
            query += " AND candidate_id = ?"
            params.append(candidate_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY application_id DESC"
        cursor.execute(query, params)
        return [self._row_to_app(row) for row in cursor.fetchall()]

    def update_status(self, application_id: int, status: str):
        cursor = self.db.cursor()
        cursor.execute("UPDATE applications SET status = ? WHERE application_id = ?", (status, application_id))
        self.db.commit()

    def _row_to_app(self, row) -> Application:
        return Application(
            application_id=row["application_id"],
            application_code=row["application_code"],
            candidate_id=row["candidate_id"],
            job_id=row["job_id"],
            applied_at=row["applied_at"],
            status=row["status"],
            eligibility_status=row["eligibility_status"],
            eligibility_remarks=row["eligibility_remarks"] or "",
        )
