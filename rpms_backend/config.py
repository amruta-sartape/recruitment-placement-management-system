"""
Recruitment & Placement Management System (RPMS)
Configuration Module
"""

import os

# Database Configuration
DB_HOST = os.environ.get("RPMS_DB_HOST", "localhost")
DB_PORT = int(os.environ.get("RPMS_DB_PORT", 3306))
DB_USER = os.environ.get("RPMS_DB_USER", "root")
DB_PASSWORD = os.environ.get("RPMS_DB_PASSWORD", "root")
DB_NAME = os.environ.get("RPMS_DB_NAME", "rpms_db")

# Application Settings
APP_NAME = "Recruitment & Placement Management System (RPMS)"
APP_VERSION = "2.0.0"
INSTITUTE_NAME = "Kiran Academy"
LOG_FILE = "rpms_activity.log"
REPORTS_DIR = "reports_output"
