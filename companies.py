# ─────────────────────────────────────────────────────────────
#  companies.py  ·  Configuration for job targets
# ─────────────────────────────────────────────────────────────

# ── Target companies (priority scoring) ──────────────────────
TARGET_COMPANIES = [
    # Big 4 Consulting
    "Deloitte", "PwC", "EY", "KPMG",
    # E-commerce
    "Amazon", "Flipkart", "Meesho",
    # Tech / Product
    "PayPal", "Microsoft", "Google",
]

# ── Job roles to search & filter ─────────────────────────────
JOB_ROLES = [
    "Data Analyst",
    "Business Analyst",
    "MIS Analyst",
    "Reporting Analyst",
]

# ── Search queries sent to job portals ───────────────────────
SEARCH_QUERIES = [
    "data analyst",
    "business analyst",
    "MIS analyst",
    "reporting analyst",
]

# ── Location ──────────────────────────────────────────────────
LOCATION        = "Bengaluru"
LOCATION_ALT    = "Bangalore"        # alternate spelling used on portals

# ── Email settings ────────────────────────────────────────────
SENDER_EMAIL    = "jobalert287@gmail.com"
RECEIVER_EMAIL  = "jobalert287@gmail.com"
EMAIL_SUBJECT   = "🔍 Daily Job Alert – Data / Business Analyst | Bengaluru"

# ── Limits ────────────────────────────────────────────────────
MAX_JOBS        = 15                 # top jobs to include in email
DAYS_OLD        = 3                  # fetch jobs posted in last N days
