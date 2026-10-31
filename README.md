# Recruitment & Placement Management System (RPMS)
### Kiran Academy — Academic & Industry Placement Enterprise Project

---

## 📌 Project Overview
The **Recruitment & Placement Management System (RPMS)** is an industry-grade business application and enterprise UI prototype developed strictly according to the curriculum and task specifications provided by **Kiran Academy**.

The system automates the complete campus recruitment lifecycle for training institutes and colleges, managing:
1. **Candidate Master & Academic Records**
2. **Corporate Employers & HR Coordinates**
3. **Placement Drive Job Requirements & Cutoff Criteria**
4. **Automated Candidate Eligibility Engine (Gatekeeper)**
5. **Application Pipelines & Duplicate Prevention**
6. **Interview Round Scheduling & Panel Feedback (1–5 Scale)**
7. **Corporate Offer Letter Issuance & Student Acceptance**
8. **Joining Verification & Day-1 Placement Confirmation**
9. **Management Relational SQL Reports & Conversion Funnels**
10. **File Handling (Audit Reports, CSV & Text Exporters)**

---

## 📂 Project Architecture & Directory Structure

```text
d:/KA project/
├── recruitment-placement-ui/               # Enterprise HTML5/CSS3 UI Prototype (12 Pages)
│   ├── login.html                          # Entry portal & role selector (Admin / Recruiter / Placement Officer)
│   ├── dashboard.html                      # Executive metrics, funnel stages, today's schedule & recent placements
│   ├── candidates.html                     # Candidate search, filters by technology/qualification, directory table
│   ├── candidate-form.html                 # Profile entry/update with strict validation message demonstrations
│   ├── candidate-details.html              # 360-degree candidate view (academics, skill stack, drive history)
│   ├── companies.html                      # Corporate hiring partners, HR contacts, active campus drives
│   ├── jobs.html                           # Active campus drive job requirements, packages, cutoff summaries
│   ├── job-form.html                       # Job creation form with eligibility cutoff thresholds (min %, backlogs)
│   ├── applications.html                   # Pipeline workbench with interactive Eligibility Engine simulator
│   ├── interviews.html                     # Interview round scheduling, meeting coordinates, evaluation roster
│   ├── placement-process.html              # 3-Tab lifecycle (Interview Feedback -> Offer Details -> Day-1 Joining)
│   ├── reports.html                        # Executive analytics, company placement share, technology distribution
│   ├── css/
│   │   └── style.css                       # Enterprise design system (Tokens, cards, badges, tables, modals)
│   └── images/
│       └── logo.svg                        # Institutional Kiran Academy vector logo
│
├── rpms_backend/                           # Python Business Backend Application (OOP Modular Architecture)
│   ├── __init__.py
│   ├── config.py                           # Database credentials & institutional constants
│   ├── main.py                             # Interactive Menu-driven CLI Console Application
│   ├── run_demo.py                         # Automated 10-Stage Lifecycle Test Suite
│   ├── database/                           # Relational persistence & connection management
│   │   ├── __init__.py
│   │   ├── connection.py                   # MySQL 8.x connector with automatic SQLite fallback
│   │   └── rpms_local.db                   # Pre-seeded local relational database
│   ├── models/                             # Domain Entities (Data Classes & Validations)
│   │   ├── __init__.py
│   │   ├── candidate.py                    # Candidate entity
│   │   ├── company.py                      # Company entity
│   │   ├── job.py                          # Job requirement entity
│   │   ├── application.py                  # Job application entity
│   │   ├── interview.py                    # InterviewRound entity
│   │   └── offer_placement.py              # Offer & Placement entities
│   ├── dao/                                # Data Access Object Layer (CRUD & Query Execution)
│   │   ├── __init__.py
│   │   ├── candidate_dao.py
│   │   ├── company_dao.py
│   │   ├── job_dao.py
│   │   ├── application_dao.py
│   │   ├── interview_dao.py
│   │   └── placement_dao.py
│   ├── services/                           # Core Business Logic Layer
│   │   ├── __init__.py
│   │   ├── eligibility_engine.py           # The Candidate Eligibility Engine
│   │   ├── recruitment_service.py          # 10-Stage end-to-end recruitment lifecycle orchestrator
│   │   └── report_service.py               # SQL aggregate queries, conversion rates, and aging reports
│   ├── validators/                         # Domain Constraint Validators
│   │   ├── __init__.py
│   │   └── business_validators.py          # 10-digit mobile, valid email regex, percentage 0-100, openings > 0
│   ├── exceptions/                         # Custom Exception Hierarchy
│   │   ├── __init__.py
│   │   └── custom_exceptions.py            # IneligibleCandidateException, DuplicateApplicationException, etc.
│   ├── utils/                              # Logging & File Handling
│   │   ├── __init__.py
│   │   ├── logger.py                       # File & console logging (rpms_activity.log)
│   │   └── export_utils.py                 # File handling: CSV roster and ASCII audit report exporter
│   └── exports/                            # Generated file handling reports
│       ├── candidates_roster.csv
│       └── placement_summary.txt
│
├── rpms_schema.sql                         # Original MySQL 8.x relational database schema (533 lines)
├── rpms_sample_data.sql                    # Comprehensive sample data script (407 lines)
├── rpms_full_setup.sql                     # Full turnkey MySQL database script
└── task_docs/                              # Original Kiran Academy task PDFs
    ├── 1553de122c6d1f072eb65374dfe2e56b2781a3bb (1).pdf  # UI Prototype Specification Document (18 Pages)
    └── Python_Recruitment_Placement_Abstract.pdf           # Python Project Abstract
```

---

## 🖥️ Part 1: How to View & Navigate the UI Prototype

The UI Prototype is located in `recruitment-placement-ui/`. It is built with technology-neutral **HTML5** and **CSS3**, requiring **no local web server or frameworks**.

### Quick Start
1. Open your web browser (Chrome, Edge, Firefox, Safari).
2. Double-click or open `d:/KA project/recruitment-placement-ui/login.html`.
3. Click **"Sign In to Dashboard &rarr;"** (prefilled with `recruiter@demo.com`).
4. Navigate through all 12 operational pages using the sidebar menu and buttons.

### Key Navigation Flows Implemented:
* **Candidate Workflow**: `login.html` &rarr; `dashboard.html` &rarr; `candidates.html` &rarr; `candidate-form.html` &rarr; `candidate-details.html` &rarr; `applications.html`
* **Job Requirement Workflow**: `dashboard.html` &rarr; `jobs.html` &rarr; `job-form.html` &rarr; `jobs.html` &rarr; `applications.html`
* **Eligibility & Application Workflow**: `applications.html` &rarr; Click **"⚡ Run Eligibility Check"** to launch the interactive live evaluation modal &rarr; Review automated checklist &rarr; Submit Application.
* **Interview Coordination Workflow**: `interviews.html` &rarr; Click **"➕ Schedule Interview"** &rarr; Submit &rarr; Click **"Submit Result"** &rarr; Redirects to `placement-process.html`.
* **Selection & Offer Workflow**: `placement-process.html` &rarr;
  * **Tab 1**: Interview Ratings (1–5 Stars) & Panel Feedback remarks &rarr; Save.
  * **Tab 2**: Corporate Offer Parameters (Designation, Offered Package, Dates) & Student Acceptance &rarr; Update Offer.
  * **Tab 3**: Day-1 Physical/Virtual Joining Verification & Corporate Employee ID &rarr; Click **"🎓 Confirm Joining & Mark Candidate PLACED"**.
* **Management Reports**: `reports.html` &rarr; View live conversion funnels, company placement share, technology track breakdown, and aging monitor. Click **"🖨️ Print Report"** or **"📥 Export PDF/Excel"**.

---

## 🐍 Part 2: How to Run the Python Backend Application

The Python backend application is developed using **Python 3.10+**, **Object-Oriented Programming (OOP)**, **Modular Packaging**, **File Handling**, and **Relational Database Connectivity**.

### Dual-Mode Database Support
* **Automatic Fallback Mode (Instant Run)**: If a local MySQL server is not running, the application automatically initializes a pre-seeded local SQLite relational database (`rpms_local.db`) populated with the exact records from `rpms_sample_data.sql`. You can run the code immediately!
* **MySQL 8.x Mode**: If you have MySQL running, configure credentials in `rpms_backend/config.py` or set environment variables (`RPMS_DB_HOST`, `RPMS_DB_USER`, `RPMS_DB_PASSWORD`, `RPMS_DB_NAME`), and execute `rpms_full_setup.sql`.

### 1. Run the Automated 10-Stage Demonstration Suite
This automated script tests and demonstrates every single requirement from the Kiran Academy abstract from start to finish:
```bash
python -m rpms_backend.run_demo
```
**Output Demonstration Highlights:**
* **Stage 1**: Registers a new candidate with full validation.
* **Stage 2**: Evaluates candidates against the **Candidate Eligibility Engine**:
  * *Test Case A*: Eligible candidate &rarr; Passes 8 rules with a 100.0/100.0 score.
  * *Test Case B*: Ineligible candidate &rarr; Fails with detailed diagnostic feedback (`59.5% < 60.0% cutoff` and `1 backlog > 0 allowed`).
* **Stage 3**: Submits application and verifies that duplicate applications are blocked.
* **Stage 4**: Shortlists candidate for interview rounds.
* **Stage 5**: Schedules Technical Round 1 interview.
* **Stage 6**: Records panel evaluation ratings (1–5 scale) and feedback notes.
* **Stage 7**: Generates corporate offer letter (5.4 LPA) and records student acceptance.
* **Stage 8**: Confirms Day-1 joining, assigns corporate employee ID (`INF-90412`), and updates candidate status to `PLACED`.
* **Stage 9**: Executes SQL relational reports (Conversion funnel, company share, technology distribution).
* **Stage 10**: Exercises Python File Handling by writing `exports/placement_summary.txt` and `exports/candidates_roster.csv`.

### 2. Launch the Interactive Console Application (CLI)
To run the interactive menu-driven console:
```bash
python -m rpms_backend.main
```
Menu options allow you to register candidates, post jobs, test eligibility combinations, record interview scores, issue offers, and export data.

---

## ✅ Acceptance Criteria & Compliance Checklist

| # | Requirement Specification | Status | Implementation Details |
|---|---------------------------|:------:|------------------------|
| 1 | All 12 HTML pages present | ✅ Passed | Fully created in `recruitment-placement-ui/` |
| 2 | Unified styling & design tokens | ✅ Passed | Shared CSS in `css/style.css` with brand colors, cards, and buttons |
| 3 | Active relative navigation | ✅ Passed | All links between dashboard, candidates, jobs, interviews, offers, and reports work |
| 4 | Realistic static sample data | ✅ Passed | Populated with 10+ candidates, 6 companies, 7 jobs, 11 applications, 8 interviews |
| 5 | Non-functional prototype boundaries | ✅ Passed | UI prototype is technology-neutral without embedded backend language tags |
| 6 | Candidate Eligibility Engine | ✅ Passed | Automated rule checker evaluating %, backlogs, year, degree, tech, and duplicate apply |
| 7 | Full recruitment lifecycle | ✅ Passed | Implemented all stages: Registration &rarr; Eligibility &rarr; Apply &rarr; Shortlist &rarr; Interview &rarr; Offer &rarr; Join &rarr; Placement |
| 8 | Python OOP & Modular Architecture | ✅ Passed | Models, DAO, Services, Validators, Exceptions, Utils separated into packages |
| 9 | Python File Handling | ✅ Passed | CSV exporter (`candidates_roster.csv`) & formatted ASCII report generator (`placement_summary.txt`) |
| 10| SQL Relational Database Queries | ✅ Passed | Schema in `rpms_schema.sql`, join queries for company-wise and technology-wise reports |

---

*Project developed for Kiran Academy Placement Cell Evaluation & Academic Curriculum.*
