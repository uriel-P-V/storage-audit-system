# Storage Audit System  

A production-inspired storage operation audit system built with Python and SQLite — 
designed to simulate real QA workflows in enterprise storage environments.

Tracks every storage operation, classifies failures, and generates audit reports 
for QA teams to identify issues and prioritize fixes.

---


# Storage Audit System

![CI](https://github.com/uriel-P-V/storage-audit-system/actions/workflows/tests.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Project Structure
 
```
storage-audit-system/
├── audit/
│   ├── __init__.py
│   ├── db.py           ← SQLite connection and schema setup
│   ├── logger.py       ← Records operations into audit_log table
│   └── reports.py      ← Generates summary and failure reports
├── tests/
│   ├── conftest.py     ← In-memory SQLite fixtures
│   ├── test_logger.py  ← 9 tests for AuditLogger
│   └── test_reports.py ← 4 tests for AuditReporter
├── scripts/
│   ├── setup_db.sh     ← Initializes the database
│   ├── audit_report.sh ← Displays audit report in terminal
│   └── seed_db.py      ← Inserts sample data
├── pytest.ini
├── requirements.txt
└── .env.example
```
 
---
## Features

- **AuditLogger** — records CREATE, READ, WRITE, DELETE operations with user and status
- **AuditReporter** — generates summaries, failure reports, and user activity
- **13 automated tests** — insertion, filtering, counting, reporting
- **In-memory SQLite** — fully isolated tests, no file cleanup needed
- **Bash scripts** — Unix-style DB setup and report generation
- **SQL Injection protection** — parameterized queries throughout

---

## Setup

```bash
git clone https://github.com/uriel-P-V/storage-audit-system.git
cd storage-audit-system
pip install -r requirements.txt
cp .env.example .env

# Initialize database
bash scripts/setup_db.sh

# Insert sample data
python scripts/seed_db.py
```

---

## Running Tests

```bash
# All tests
pytest

# By marker
pytest -m smoke
pytest -m critical
pytest -m regression
```

---

## Audit Report
 
```bash
bash scripts/audit_report.sh
```
 
Output example:
 
```
========================================
  Storage Audit Report
  DB: audit.db
========================================
  Total operations : 7
  Successful       : 4
  Failed           : 3
  Pass rate        : 57.1%
 
  --- Recent Failures ---
  [CREATE] /vol/backup by admin — Disk full
  [WRITE]  /vol/backup by system — Disk full
  [DELETE] /vol/temp by uriel — Permission denied
 
  --- Top Paths with Failures ---
  /vol/backup — 2 failure(s)
  /vol/temp — 1 failure(s)
========================================
```
 
---
## Agile Workflow

- Features developed in **feature branches**
- Code reviewed via **Pull Requests** before merging
- Conventional commits: `feat:`, `fix:`, `test:`, `docs:`

---

## Tech Stack

- **Python 3.10+**
- **SQLite** — embedded database, no server required
- **Pytest** — test framework with fixtures and markers
- **Bash** — Unix scripting for DB management and reporting

---

## Author

**Uriel Alejandro Pérez Valdovinos**  
[github.com/uriel-P-V](https://github.com/uriel-P-V) · [linkedin.com/in/uriel-pv](https://linkedin.com/in/uriel-pv)