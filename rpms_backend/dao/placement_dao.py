"""
Placement & Offer Data Access Object (DAO)
Performs database operations for corporate offers and final placement records
"""

from typing import List, Optional
from rpms_backend.database import DatabaseManager
from rpms_backend.models import Offer, Placement

class PlacementDAO:
    def __init__(self):
        self.db = DatabaseManager.get_instance().get_connection()

    def save_offer(self, offer: Offer) -> Offer:
        cursor = self.db.cursor()
        if offer.offer_id:
            query = "UPDATE offers SET status = ?, remarks = ? WHERE offer_id = ?"
            cursor.execute(query, (offer.status, offer.remarks, offer.offer_id))
        else:
            if not offer.offer_code:
                cursor.execute("SELECT COUNT(*) FROM offers")
                count = cursor.fetchone()[0] + 1
                offer.offer_code = f"OFF-2026-{count:04d}"

            query = """
            INSERT INTO offers (
                offer_code, application_id, candidate_id, company_id, job_id,
                offered_role, offered_package, offer_date, expected_joining_date,
                status, remarks
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                offer.offer_code, offer.application_id, offer.candidate_id,
                offer.company_id, offer.job_id, offer.offered_role,
                offer.offered_package, str(offer.offer_date),
                str(offer.expected_joining_date), offer.status, offer.remarks
            ))
            offer.offer_id = cursor.lastrowid

        self.db.commit()
        return offer

    def get_offer_by_id(self, offer_id: int) -> Optional[Offer]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM offers WHERE offer_id = ?", (offer_id,))
        row = cursor.fetchone()
        return self._row_to_offer(row) if row else None

    def get_offer_by_application(self, application_id: int) -> Optional[Offer]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM offers WHERE application_id = ?", (application_id,))
        row = cursor.fetchone()
        return self._row_to_offer(row) if row else None

    def get_all_offers(self) -> List[Offer]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM offers ORDER BY offer_id DESC")
        return [self._row_to_offer(row) for row in cursor.fetchall()]

    def save_placement(self, placement: Placement) -> Placement:
        cursor = self.db.cursor()
        if not placement.placement_code:
            cursor.execute("SELECT COUNT(*) FROM placements")
            count = cursor.fetchone()[0] + 1
            placement.placement_code = f"PLC-2026-{count:04d}"

        query = """
        INSERT INTO placements (
            placement_code, offer_id, candidate_id, company_id, job_id,
            designation, package_offered, actual_joining_date, joining_status,
            corporate_emp_id, placement_officer, remarks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            placement.placement_code, placement.offer_id, placement.candidate_id,
            placement.company_id, placement.job_id, placement.designation,
            placement.package_offered, str(placement.actual_joining_date),
            placement.joining_status, placement.corporate_emp_id,
            placement.placement_officer, placement.remarks
        ))
        placement.placement_id = cursor.lastrowid
        self.db.commit()
        return placement

    def get_all_placements(self) -> List[Placement]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM placements ORDER BY placement_id DESC")
        return [self._row_to_placement(row) for row in cursor.fetchall()]

    def _row_to_offer(self, row) -> Offer:
        return Offer(
            offer_id=row["offer_id"],
            offer_code=row["offer_code"],
            application_id=row["application_id"],
            candidate_id=row["candidate_id"],
            company_id=row["company_id"],
            job_id=row["job_id"],
            offered_role=row["offered_role"],
            offered_package=float(row["offered_package"]),
            offer_date=row["offer_date"],
            expected_joining_date=row["expected_joining_date"],
            status=row["status"],
            remarks=row["remarks"] or "",
        )

    def _row_to_placement(self, row) -> Placement:
        return Placement(
            placement_id=row["placement_id"],
            placement_code=row["placement_code"],
            offer_id=row["offer_id"],
            candidate_id=row["candidate_id"],
            company_id=row["company_id"],
            job_id=row["job_id"],
            designation=row["designation"],
            package_offered=float(row["package_offered"]),
            actual_joining_date=row["actual_joining_date"],
            joining_status=row["joining_status"],
            corporate_emp_id=row["corporate_emp_id"] or "",
            placement_officer=row["placement_officer"] or "Neha Deshmukh",
            remarks=row["remarks"] or "",
        )
