"""
Candidate Data Access Object (DAO)
Performs database operations for candidate master records
"""

from typing import List, Optional
from rpms_backend.database import DatabaseManager
from rpms_backend.models import Candidate

class CandidateDAO:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def save(self, candidate: Candidate) -> Candidate:
        candidate.validate()
        cursor = self.db.cursor()
        
        if candidate.candidate_id:
            query = """
            UPDATE candidates SET
                full_name = ?, email = ?, mobile = ?, qualification = ?,
                college = ?, university = ?, passing_year = ?, percentage = ?,
                backlog_count = ?, primary_technology = ?, current_location = ?,
                preferred_location = ?, profile_status = ?, placement_status = ?
            WHERE candidate_id = ?
            """
            cursor.execute(query, (
                candidate.full_name, candidate.email, candidate.mobile, candidate.qualification,
                candidate.college, candidate.university, candidate.passing_year, candidate.percentage,
                candidate.backlog_count, candidate.primary_technology, candidate.current_location,
                candidate.preferred_location, candidate.profile_status, candidate.placement_status,
                candidate.candidate_id
            ))
        else:
            if not candidate.candidate_code:
                # Generate unique candidate code
                cursor.execute("SELECT COUNT(*) FROM candidates")
                count = cursor.fetchone()[0] + 1
                candidate.candidate_code = f"CAN-2026-{count:04d}"

            query = """
            INSERT INTO candidates (
                candidate_code, full_name, email, mobile, date_of_birth, gender,
                qualification, college, university, passing_year, percentage,
                backlog_count, primary_technology, current_location, preferred_location,
                profile_status, placement_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                candidate.candidate_code, candidate.full_name, candidate.email, candidate.mobile,
                str(candidate.date_of_birth) if candidate.date_of_birth else None, candidate.gender,
                candidate.qualification, candidate.college, candidate.university, candidate.passing_year,
                candidate.percentage, candidate.backlog_count, candidate.primary_technology,
                candidate.current_location, candidate.preferred_location, candidate.profile_status,
                candidate.placement_status
            ))
            candidate.candidate_id = cursor.lastrowid

        self.db.commit()
        return candidate

    def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,))
        row = cursor.fetchone()
        return self._row_to_candidate(row) if row else None

    def get_by_code(self, candidate_code: str) -> Optional[Candidate]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM candidates WHERE candidate_code = ?", (candidate_code,))
        row = cursor.fetchone()
        return self._row_to_candidate(row) if row else None

    def get_by_email(self, email: str) -> Optional[Candidate]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM candidates WHERE email = ?", (email.strip(),))
        row = cursor.fetchone()
        return self._row_to_candidate(row) if row else None

    def get_all(self, technology: str = None, passing_year: int = None, status: str = None) -> List[Candidate]:
        cursor = self.db.cursor()
        query = "SELECT * FROM candidates WHERE 1=1"
        params = []

        if technology:
            query += " AND primary_technology = ?"
            params.append(technology)
        if passing_year:
            query += " AND passing_year = ?"
            params.append(passing_year)
        if status:
            query += " AND placement_status = ?"
            params.append(status)

        query += " ORDER BY candidate_id ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [self._row_to_candidate(row) for row in rows]

    def update_placement_status(self, candidate_id: int, status: str):
        cursor = self.db.cursor()
        cursor.execute("UPDATE candidates SET placement_status = ? WHERE candidate_id = ?", (status, candidate_id))
        self.db.commit()

    def _row_to_candidate(self, row) -> Candidate:
        return Candidate(
            candidate_id=row["candidate_id"],
            candidate_code=row["candidate_code"],
            full_name=row["full_name"],
            email=row["email"],
            mobile=row["mobile"],
            date_of_birth=row["date_of_birth"],
            gender=row["gender"] or "Male",
            qualification=row["qualification"],
            college=row["college"],
            university=row["university"] or "",
            passing_year=row["passing_year"],
            percentage=float(row["percentage"]),
            backlog_count=int(row["backlog_count"]),
            primary_technology=row["primary_technology"],
            current_location=row["current_location"] or "Pune",
            preferred_location=row["preferred_location"] or "Pune",
            profile_status=row["profile_status"],
            placement_status=row["placement_status"],
        )
