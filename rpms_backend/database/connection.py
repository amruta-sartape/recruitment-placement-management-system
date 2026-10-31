"""
Database Connection Manager for RPMS
Supports MySQL 8.x connectivity with transparent SQLite fallback
"""

import sqlite3
import os
import sys
from rpms_backend import config

class DatabaseManager:
    _instance = None
    _connection = None
    _is_mysql = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._init_connection()

    def _init_connection(self):
        # Try MySQL connection first if driver is installed
        mysql_driver = None
        try:
            import mysql.connector
            mysql_driver = "mysql.connector"
        except ImportError:
            try:
                import pymysql
                mysql_driver = "pymysql"
            except ImportError:
                mysql_driver = None

        if mysql_driver:
            try:
                if mysql_driver == "mysql.connector":
                    import mysql.connector
                    self._connection = mysql.connector.connect(
                        host=config.DB_HOST,
                        port=config.DB_PORT,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        database=config.DB_NAME,
                        autocommit=False
                    )
                elif mysql_driver == "pymysql":
                    import pymysql
                    self._connection = pymysql.connect(
                        host=config.DB_HOST,
                        port=config.DB_PORT,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        database=config.DB_NAME,
                        autocommit=False
                    )
                self._is_mysql = True
                return
            except Exception as e:
                # Local MySQL server not actively running; fall back to SQLite relational DB
                pass

        # Fallback to local SQLite database seeded with full schema & sample data
        db_path = os.path.join(os.path.dirname(__file__), "rpms_local.db")
        is_new = not os.path.exists(db_path)
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._is_mysql = False

        if is_new:
            self._seed_sqlite_database()

    def _seed_sqlite_database(self):
        """Creates the relational tables and populates realistic records"""
        cursor = self._connection.cursor()
        
        # Schema definition
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS qualifications (
            qualification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            qualification_name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL,
            state_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_code TEXT NOT NULL UNIQUE,
            role_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE,
            role_id INTEGER,
            status TEXT DEFAULT 'ACTIVE'
        );

        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_code TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            mobile TEXT NOT NULL UNIQUE,
            date_of_birth TEXT,
            gender TEXT,
            qualification TEXT NOT NULL,
            college TEXT NOT NULL,
            university TEXT,
            passing_year INTEGER NOT NULL,
            percentage REAL NOT NULL,
            cgpa REAL,
            backlog_count INTEGER NOT NULL DEFAULT 0,
            primary_technology TEXT NOT NULL,
            current_location TEXT,
            preferred_location TEXT,
            profile_status TEXT DEFAULT 'ACTIVE',
            placement_status TEXT DEFAULT 'NOT_PLACED'
        );

        CREATE TABLE IF NOT EXISTS candidate_skills (
            candidate_id INTEGER,
            skill_name TEXT NOT NULL,
            PRIMARY KEY (candidate_id, skill_name)
        );

        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_code TEXT NOT NULL UNIQUE,
            company_name TEXT NOT NULL,
            industry TEXT NOT NULL,
            company_type TEXT DEFAULT 'MNC',
            website TEXT,
            location TEXT NOT NULL,
            hr_name TEXT NOT NULL,
            hr_email TEXT NOT NULL,
            hr_mobile TEXT,
            status TEXT DEFAULT 'ACTIVE'
        );

        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_code TEXT NOT NULL UNIQUE,
            company_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            openings INTEGER NOT NULL,
            employment_type TEXT DEFAULT 'Full-time',
            location TEXT NOT NULL,
            min_package REAL,
            max_package REAL,
            allowed_qualifications TEXT NOT NULL,
            min_percentage REAL NOT NULL,
            min_passing_year INTEGER,
            max_passing_year INTEGER,
            max_backlogs INTEGER NOT NULL DEFAULT 0,
            required_technology TEXT NOT NULL,
            required_skills TEXT,
            posted_date TEXT NOT NULL,
            deadline_date TEXT NOT NULL,
            status TEXT DEFAULT 'OPEN'
        );

        CREATE TABLE IF NOT EXISTS applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_code TEXT NOT NULL UNIQUE,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            applied_at TEXT NOT NULL,
            status TEXT DEFAULT 'APPLIED',
            eligibility_status TEXT DEFAULT 'PENDING',
            eligibility_remarks TEXT,
            UNIQUE(candidate_id, job_id)
        );

        CREATE TABLE IF NOT EXISTS interview_rounds (
            interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_code TEXT NOT NULL UNIQUE,
            application_id INTEGER NOT NULL,
            round_name TEXT NOT NULL,
            scheduled_date TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            mode TEXT DEFAULT 'Online',
            interviewer_name TEXT,
            meeting_url TEXT,
            status TEXT DEFAULT 'SCHEDULED',
            tech_rating REAL,
            comm_rating REAL,
            problem_rating REAL,
            overall_rating REAL,
            feedback_remarks TEXT,
            result TEXT DEFAULT 'PENDING'
        );

        CREATE TABLE IF NOT EXISTS offers (
            offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_code TEXT NOT NULL UNIQUE,
            application_id INTEGER NOT NULL UNIQUE,
            candidate_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            offered_role TEXT NOT NULL,
            offered_package REAL NOT NULL,
            offer_date TEXT NOT NULL,
            expected_joining_date TEXT NOT NULL,
            status TEXT DEFAULT 'OFFERED',
            remarks TEXT
        );

        CREATE TABLE IF NOT EXISTS placements (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            placement_code TEXT NOT NULL UNIQUE,
            offer_id INTEGER NOT NULL UNIQUE,
            candidate_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            designation TEXT NOT NULL,
            package_offered REAL NOT NULL,
            actual_joining_date TEXT NOT NULL,
            joining_status TEXT DEFAULT 'JOINED',
            corporate_emp_id TEXT,
            placement_officer TEXT DEFAULT 'Neha Deshmukh',
            remarks TEXT
        );
        """)

        # Seed realistic records matching rpms_sample_data.sql
        cursor.executescript("""
        INSERT OR IGNORE INTO roles (role_id, role_code, role_name) VALUES
        (1, 'ADMIN', 'System Administrator'),
        (2, 'RECRUITER', 'Campus Recruiter'),
        (3, 'PLACEMENT_OFFICER', 'Placement Officer');

        INSERT OR IGNORE INTO users (user_id, username, full_name, email, role_id, status) VALUES
        (1, 'admin', 'System Admin', 'admin@kiranacademy.com', 1, 'ACTIVE'),
        (2, 'amit.recruiter', 'Amit Kulkarni', 'amit.recruiter@kiranacademy.com', 2, 'ACTIVE'),
        (3, 'sneha.recruiter', 'Sneha Patil', 'sneha.recruiter@kiranacademy.com', 2, 'ACTIVE'),
        (4, 'neha.placement', 'Neha Deshmukh', 'neha.placement@kiranacademy.com', 3, 'ACTIVE');

        INSERT OR IGNORE INTO companies (company_id, company_code, company_name, industry, company_type, website, location, hr_name, hr_email, hr_mobile, status) VALUES
        (1, 'COM-101', 'Infosys Limited', 'IT Services', 'MNC', 'https://www.infosys.com', 'Pune', 'Priya Sharma', 'priya.sharma@infosys.com', '9823011223', 'ACTIVE'),
        (2, 'COM-102', 'Tata Consultancy Services', 'IT Services', 'MNC', 'https://www.tcs.com', 'Mumbai', 'Rajesh Nair', 'rajesh.nair@tcs.com', '9823022334', 'ACTIVE'),
        (3, 'COM-103', 'Wipro Limited', 'IT Services', 'MNC', 'https://www.wipro.com', 'Bengaluru', 'Anand Verma', 'anand.verma@wipro.com', '9823033445', 'ACTIVE'),
        (4, 'COM-104', 'Capgemini', 'Consulting', 'MNC', 'https://www.capgemini.com', 'Pune', 'Meera Joshi', 'meera.joshi@capgemini.com', '9823044556', 'ACTIVE'),
        (5, 'COM-105', 'Persistent Systems', 'Product Engineering', 'Mid-size', 'https://www.persistent.com', 'Pune', 'Sunil Patil', 'sunil.patil@persistent.com', '9823055667', 'ACTIVE'),
        (6, 'COM-106', 'Cognizant', 'IT Services', 'MNC', 'https://www.cognizant.com', 'Hyderabad', 'Divya Rao', 'divya.rao@cognizant.com', '9823066778', 'ACTIVE');

        INSERT OR IGNORE INTO candidates (candidate_id, candidate_code, full_name, email, mobile, date_of_birth, gender, qualification, college, university, passing_year, percentage, backlog_count, primary_technology, current_location, preferred_location, profile_status, placement_status) VALUES
        (1, 'CAN-2026-0001', 'Rahul Patil', 'rahul.patil01@example.com', '9000000001', '2002-04-12', 'Male', 'BE', 'ABC College Pune', 'SPPU', 2025, 68.5, 0, 'Java', 'Pune', 'Pune', 'ACTIVE', 'NOT_PLACED'),
        (2, 'CAN-2026-0002', 'Sneha More', 'sneha.more02@example.com', '9000000002', '2002-08-21', 'Female', 'BTech', 'Modern College', 'SPPU', 2025, 74.2, 0, 'Python', 'Pune', 'Bengaluru', 'ACTIVE', 'NOT_PLACED'),
        (3, 'CAN-2026-0003', 'Amit Shinde', 'amit.shinde03@example.com', '9000000003', '2001-12-02', 'Male', 'MCA', 'MIT College', 'SPPU', 2024, 71.0, 0, 'Java', 'Pune', 'Pune', 'ACTIVE', 'NOT_PLACED'),
        (4, 'CAN-2026-0004', 'Neha Jadhav', 'neha.jadhav04@example.com', '9000000004', '2002-06-13', 'Female', 'BE', 'DY Patil College', 'SPPU', 2025, 82.4, 0, 'Python', 'Pimpri', 'Pune', 'ACTIVE', 'NOT_PLACED'),
        (5, 'CAN-2026-0005', 'Rohit Pawar', 'rohit.pawar05@example.com', '9000000005', '2002-03-03', 'Male', 'BTech', 'PCCOE', 'SPPU', 2025, 59.5, 1, 'Java', 'Pimpri', 'Pune', 'ACTIVE', 'NOT_PLACED'),
        (6, 'CAN-2026-0006', 'Priya Desai', 'priya.desai06@example.com', '9000000006', '2001-09-17', 'Female', 'MCA', 'Fergusson College', 'SPPU', 2024, 76.1, 0, 'Python', 'Pune', 'Hyderabad', 'ACTIVE', 'NOT_PLACED'),
        (7, 'CAN-2026-0007', 'Akash Kale', 'akash.kale07@example.com', '9000000007', '2002-10-11', 'Male', 'BE', 'Sinhgad College', 'SPPU', 2025, 64.8, 0, 'Testing', 'Pune', 'Pune', 'ACTIVE', 'NOT_PLACED'),
        (8, 'CAN-2026-0008', 'Pooja Mali', 'pooja.mali08@example.com', '9000000008', '2002-02-24', 'Female', 'BCA', 'Indira College', 'SPPU', 2025, 72.6, 0, 'Data Analytics', 'Pune', 'Mumbai', 'ACTIVE', 'NOT_PLACED'),
        (9, 'CAN-2026-0010', 'Komal Gaikwad', 'komal.gaikwad10@example.com', '9000000010', '2002-05-09', 'Female', 'BE', 'AISSMS Pune', 'SPPU', 2025, 78.9, 0, 'Java', 'Pune', 'Bengaluru', 'ACTIVE', 'PLACED'),
        (10, 'CAN-2026-0014', 'Rutuja Salunkhe', 'rutuja.salunkhe14@example.com', '9000000014', '2002-09-23', 'Female', 'BTech', 'PCCOE', 'SPPU', 2025, 85.0, 0, 'Data Analytics', 'Pimpri', 'Pune', 'ACTIVE', 'PLACED');

        INSERT OR IGNORE INTO jobs (job_id, job_code, company_id, job_title, openings, employment_type, location, min_package, max_package, allowed_qualifications, min_percentage, min_passing_year, max_passing_year, max_backlogs, required_technology, required_skills, posted_date, deadline_date, status) VALUES
        (1, 'JOB-2026-001', 1, 'Associate Java Developer', 15, 'Full-time', 'Pune', 4.5, 6.0, 'BE,BTech,MCA', 60.0, 2024, 2026, 0, 'Java', 'Java,SQL,JDBC,Spring', '2026-10-20', '2026-11-15', 'OPEN'),
        (2, 'JOB-2026-002', 2, 'Software Engineer - Python & Full Stack', 20, 'Full-time', 'Pune', 4.0, 5.5, 'BE,BTech,MCA', 65.0, 2025, 2025, 0, 'Python', 'Python,MySQL,Django', '2026-10-22', '2026-11-20', 'OPEN'),
        (3, 'JOB-2026-003', 3, 'Project Engineer - QA & Testing', 12, 'Full-time', 'Bengaluru', 3.8, 4.5, 'BE,BTech,MCA,BSc Computer Science', 60.0, 2024, 2025, 1, 'Testing', 'Selenium,Manual,JIRA', '2026-10-24', '2026-11-25', 'OPEN'),
        (4, 'JOB-2026-004', 4, 'Junior Cloud & Java Trainee', 25, 'Full-time', 'Pune', 4.25, 5.0, 'BE,BTech,MCA', 60.0, 2025, 2025, 0, 'Java', 'Java,Spring Boot,MySQL', '2026-10-21', '2026-11-18', 'OPEN'),
        (5, 'JOB-2026-005', 5, 'Data Analyst & BI Specialist', 10, 'Full-time', 'Pune', 5.0, 7.0, 'BE,BTech,MCA,BCA', 65.0, 2024, 2025, 0, 'Data Analytics', 'SQL,Power BI,Python,Tableau', '2026-10-18', '2026-11-12', 'OPEN');

        INSERT OR IGNORE INTO applications (application_id, application_code, candidate_id, job_id, applied_at, status, eligibility_status, eligibility_remarks) VALUES
        (1, 'APP-2026-0001', 1, 1, '2026-10-20 10:30:00', 'SHORTLISTED', 'ELIGIBLE', 'Met qualification, 68.5% >= 60.0%, 0 backlogs, Java track matched'),
        (2, 'APP-2026-0002', 2, 2, '2026-10-22 14:15:00', 'INTERVIEW_SCHEDULED', 'ELIGIBLE', 'Met qualification, 74.2% >= 65.0%, 0 backlogs, Python track matched'),
        (3, 'APP-2026-0003', 3, 1, '2026-10-21 11:00:00', 'SHORTLISTED', 'ELIGIBLE', 'Met qualification MCA, 71.0% >= 60.0%, 0 backlogs'),
        (4, 'APP-2026-0004', 4, 4, '2026-10-23 09:45:00', 'INTERVIEW_SCHEDULED', 'ELIGIBLE', 'Met qualification, 82.4% >= 60.0%, 0 backlogs'),
        (5, 'APP-2026-0005', 5, 1, '2026-10-21 16:20:00', 'REJECTED', 'INELIGIBLE', 'Criteria failed: Percentage 59.5% < 60.0% cutoff AND 1 backlog > 0 allowed'),
        (6, 'APP-2026-0006', 6, 5, '2026-10-19 12:10:00', 'SELECTED', 'ELIGIBLE', 'Cleared technical & HR rounds'),
        (7, 'APP-2026-0007', 7, 3, '2026-10-24 15:30:00', 'ELIGIBLE', 'ELIGIBLE', 'Met qualification, 64.8% >= 60.0%, 0 backlogs <= 1 allowed');

        INSERT OR IGNORE INTO interview_rounds (interview_id, interview_code, application_id, round_name, scheduled_date, scheduled_time, mode, interviewer_name, status, tech_rating, comm_rating, problem_rating, overall_rating, feedback_remarks, result) VALUES
        (1, 'INT-2026-0001', 1, 'Technical Round 1', '2026-10-25', '11:00', 'Online', 'Vikas Jadhav', 'COMPLETED', 5.0, 4.0, 4.0, 4.5, 'Strong OOP, Java Collections, and SQL joins', 'SELECTED'),
        (2, 'INT-2026-0002', 1, 'HR Round', '2026-10-30', '15:00', 'Online', 'Priya Sharma', 'SCHEDULED', NULL, NULL, NULL, NULL, '', 'PENDING'),
        (3, 'INT-2026-0003', 2, 'Aptitude Test', '2026-10-30', '11:30', 'Offline', 'Amit Kulkarni', 'SCHEDULED', NULL, NULL, NULL, NULL, '', 'PENDING');

        INSERT OR IGNORE INTO offers (offer_id, offer_code, application_id, candidate_id, company_id, job_id, offered_role, offered_package, offer_date, expected_joining_date, status, remarks) VALUES
        (1, 'OFF-2026-0001', 1, 1, 1, 1, 'Associate Java Developer', 5.2, '2026-10-30', '2026-12-01', 'ACCEPTED', 'Includes 12-month training bond'),
        (2, 'OFF-2026-0002', 6, 6, 5, 5, 'Data Analyst', 5.5, '2026-10-28', '2026-12-15', 'OFFERED', 'Awaiting candidate acceptance');

        INSERT OR IGNORE INTO placements (placement_id, placement_code, offer_id, candidate_id, company_id, job_id, designation, package_offered, actual_joining_date, joining_status, corporate_emp_id, placement_officer, remarks) VALUES
        (1, 'PLC-2026-0001', 1, 9, 1, 1, 'Java Specialist Engineer', 5.4, '2026-10-22', 'JOINED', 'INF-88102', 'Neha Deshmukh', 'Joined Pune Hinjawadi Campus'),
        (2, 'PLC-2026-0002', 2, 10, 5, 5, 'Data Analytics Engineer', 6.5, '2026-10-25', 'JOINED', 'PER-77291', 'Neha Deshmukh', 'Joined Pune Senapati Bapat Road');
        """)

        self._connection.commit()

    def get_connection(self):
        return self._connection

    def is_mysql(self):
        return self._is_mysql
