"""
Interview Round Data Access Object (DAO)
Performs database operations for evaluation rounds and interview feedback
"""

from typing import List, Optional
from rpms_backend.database import DatabaseManager
from rpms_backend.models import InterviewRound

class InterviewDAO:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def save(self, interview: InterviewRound) -> InterviewRound:
        cursor = self.db.cursor()

        if interview.interview_id:
            query = """
            UPDATE interview_rounds SET
                status = ?, tech_rating = ?, comm_rating = ?, problem_rating = ?,
                overall_rating = ?, feedback_remarks = ?, result = ?
            WHERE interview_id = ?
            """
            cursor.execute(query, (
                interview.status, interview.tech_rating, interview.comm_rating,
                interview.problem_rating, interview.overall_rating,
                interview.feedback_remarks, interview.result, interview.interview_id
            ))
        else:
            if not interview.interview_code:
                cursor.execute("SELECT COUNT(*) FROM interview_rounds")
                count = cursor.fetchone()[0] + 1
                interview.interview_code = f"INT-2026-{count:04d}"

            query = """
            INSERT INTO interview_rounds (
                interview_code, application_id, round_name, scheduled_date,
                scheduled_time, mode, interviewer_name, meeting_url, status,
                tech_rating, comm_rating, problem_rating, overall_rating,
                feedback_remarks, result
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                interview.interview_code, interview.application_id, interview.round_name,
                str(interview.scheduled_date) if interview.scheduled_date else None,
                str(interview.scheduled_time) if interview.scheduled_time else None,
                interview.mode, interview.interviewer_name, interview.meeting_url,
                interview.status, interview.tech_rating, interview.comm_rating,
                interview.problem_rating, interview.overall_rating,
                interview.feedback_remarks, interview.result
            ))
            interview.interview_id = cursor.lastrowid

        self.db.commit()
        return interview

    def get_by_id(self, interview_id: int) -> Optional[InterviewRound]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM interview_rounds WHERE interview_id = ?", (interview_id,))
        row = cursor.fetchone()
        return self._row_to_interview(row) if row else None

    def get_by_application_id(self, application_id: int) -> List[InterviewRound]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM interview_rounds WHERE application_id = ? ORDER BY interview_id ASC", (application_id,))
        return [self._row_to_interview(row) for row in cursor.fetchall()]

    def get_all(self, status: str = None) -> List[InterviewRound]:
        cursor = self.db.cursor()
        query = "SELECT * FROM interview_rounds WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY interview_id DESC"
        cursor.execute(query, params)
        return [self._row_to_interview(row) for row in cursor.fetchall()]

    def _row_to_interview(self, row) -> InterviewRound:
        return InterviewRound(
            interview_id=row["interview_id"],
            interview_code=row["interview_code"],
            application_id=row["application_id"],
            round_name=row["round_name"],
            scheduled_date=row["scheduled_date"],
            scheduled_time=row["scheduled_time"],
            mode=row["mode"],
            interviewer_name=row["interviewer_name"] or "",
            meeting_url=row["meeting_url"] or "",
            status=row["status"],
            tech_rating=row["tech_rating"],
            comm_rating=row["comm_rating"],
            problem_rating=row["problem_rating"],
            overall_rating=row["overall_rating"],
            feedback_remarks=row["feedback_remarks"] or "",
            result=row["result"],
        )
