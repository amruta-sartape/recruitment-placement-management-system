"""
RPMS File Handling and Export Utility
Exports reports and candidate data to CSV and formatted text files
"""

import os
import csv
from datetime import datetime

class ReportExporter:
    @staticmethod
    def export_to_csv(data: list, filename: str, fieldnames: list = None) -> str:
        """Exports tabular list of dictionaries to a CSV file"""
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        if not data:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                f.write("No records to display.\n")
            return file_path

        if not fieldnames:
            fieldnames = list(data[0].keys())

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        return file_path

    @staticmethod
    def export_summary_text(funnel_stats: dict, company_report: list, tech_report: list, filename: str = "placement_summary.txt") -> str:
        """Generates comprehensive ASCII text report file"""
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("=" * 72 + "\n")
            f.write("    KIRAN ACADEMY - RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM\n")
            f.write(f"           AUDIT REPORT GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 72 + "\n\n")

            f.write("1. RECRUITMENT CONVERSION FUNNEL METRICS:\n")
            f.write("-" * 45 + "\n")
            f.write(f"  Total Candidates Registered : {funnel_stats.get('total_candidates', 0):,}\n")
            f.write(f"  Total Applications Filed    : {funnel_stats.get('total_applications', 0):,}\n")
            f.write(f"  Eligible Candidates Passed  : {funnel_stats.get('eligible_applications', 0):,}\n")
            f.write(f"  Candidates Shortlisted      : {funnel_stats.get('shortlisted_applications', 0):,}\n")
            f.write(f"  Interview Rounds Conducted  : {funnel_stats.get('interviewed_candidates', 0):,}\n")
            f.write(f"  Candidates Selected         : {funnel_stats.get('selected_candidates', 0):,}\n")
            f.write(f"  Verified Final Placements   : {funnel_stats.get('placed_candidates', 0):,}\n")
            f.write(f"  Offer-to-Join Conversion    : {funnel_stats.get('offer_to_join_ratio', 0.0)}%\n\n")

            f.write("2. COMPANY-WISE PLACEMENT SHARE:\n")
            f.write("-" * 72 + "\n")
            f.write(f"{'Company Name':<32} {'Industry':<20} {'Placed':<8} {'Avg CTC':<10}\n")
            f.write("-" * 72 + "\n")
            for c in company_report:
                f.write(f"{c['company_name']:<32} {c['industry']:<20} {c['total_placed']:<8} {c['avg_package']:.2f} LPA\n")
            f.write("\n")

            f.write("3. TECHNOLOGY TRACK DISTRIBUTION:\n")
            f.write("-" * 55 + "\n")
            f.write(f"{'Technology Specialization':<30} {'Placed':<10} {'Highest CTC':<12}\n")
            f.write("-" * 55 + "\n")
            for t in tech_report:
                f.write(f"{t['technology']:<30} {t['total_placed']:<10} {t['max_package']:.2f} LPA\n")
            f.write("\n")
            f.write("=" * 72 + "\n")
            f.write("End of Official Institutional Report\n")

        return file_path
