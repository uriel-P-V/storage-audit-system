"""
seed_db.py
----------
Inserts sample audit data for testing the report script.
Run once after setup_db.sh.

Usage:
    python scripts/seed_db.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from audit.logger import AuditLogger
from audit.db import get_connection

conn = get_connection("audit.db")
logger = AuditLogger(conn=conn)

# Sample operations
logger.log("CREATE", "/vol/production",  "success", user="uriel",  message="Volume created")
logger.log("WRITE",  "/vol/production",  "success", user="uriel",  message="Data written")
logger.log("READ",   "/vol/production",  "success", user="admin",  message="Backup read")
logger.log("DELETE", "/vol/temp",        "failed",  user="uriel",  message="Permission denied")
logger.log("WRITE",  "/vol/backup",      "failed",  user="system", message="Disk full")
logger.log("CREATE", "/vol/backup",      "failed",  user="admin",  message="Disk full")
logger.log("READ",   "/vol/backup",      "success", user="uriel",  message="Read OK")

print("Sample data inserted — 7 operations (4 success, 3 failed)")