"""
Company Data Access Object (DAO)
Performs database operations for corporate employer records
"""

from typing import List, Optional
from rpms_backend.database import DatabaseManager
from rpms_backend.models import Company

class CompanyDAO:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def save(self, company: Company) -> Company:
        cursor = self.db.cursor()
        if company.company_id:
            query = """
            UPDATE companies SET
                company_name = ?, industry = ?, company_type = ?, website = ?,
                location = ?, hr_name = ?, hr_email = ?, hr_mobile = ?, status = ?
            WHERE company_id = ?
            """
            cursor.execute(query, (
                company.company_name, company.industry, company.company_type,
                company.website, company.location, company.hr_name,
                company.hr_email, company.hr_mobile, company.status,
                company.company_id
            ))
        else:
            if not company.company_code:
                cursor.execute("SELECT COUNT(*) FROM companies")
                count = cursor.fetchone()[0] + 1
                company.company_code = f"COM-{count+100:03d}"

            query = """
            INSERT INTO companies (
                company_code, company_name, industry, company_type, website,
                location, hr_name, hr_email, hr_mobile, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                company.company_code, company.company_name, company.industry,
                company.company_type, company.website, company.location,
                company.hr_name, company.hr_email, company.hr_mobile,
                company.status
            ))
            company.company_id = cursor.lastrowid

        self.db.commit()
        return company

    def get_by_id(self, company_id: int) -> Optional[Company]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM companies WHERE company_id = ?", (company_id,))
        row = cursor.fetchone()
        return self._row_to_company(row) if row else None

    def get_all(self, industry: str = None, status: str = None) -> List[Company]:
        cursor = self.db.cursor()
        query = "SELECT * FROM companies WHERE 1=1"
        params = []
        if industry:
            query += " AND industry = ?"
            params.append(industry)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY company_id ASC"
        cursor.execute(query, params)
        return [self._row_to_company(row) for row in cursor.fetchall()]

    def _row_to_company(self, row) -> Company:
        return Company(
            company_id=row["company_id"],
            company_code=row["company_code"],
            company_name=row["company_name"],
            industry=row["industry"],
            company_type=row["company_type"] or "MNC",
            website=row["website"] or "",
            location=row["location"],
            hr_name=row["hr_name"],
            hr_email=row["hr_email"],
            hr_mobile=row["hr_mobile"] or "",
            status=row["status"],
        )
