"""
NovaNotes — Shared configuration constants.
Edit these values to tune the platform behaviour.
"""

import os

# Absolute path to the novanotes/ package — used to resolve file paths
# stored as repo-relative strings (e.g. "static/demo_files/foo.pdf"), so
# downloads work regardless of the process's current working directory.
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────
# University email gate
# ──────────────────────────────────────────────
ALLOWED_EMAIL_DOMAIN = "novasbe.pt"

# ──────────────────────────────────────────────
# Points economy
# ──────────────────────────────────────────────
INITIAL_POINTS = 20        # bonus on signup
POINTS_PER_UPLOAD = 10     # earned when uploading a note
POINTS_PER_DOWNLOAD = 5    # spent when downloading a note
POINTS_PER_UPVOTE = 2      # earned when someone rates your note ≥ 4 stars

# ──────────────────────────────────────────────
# File uploads
# ──────────────────────────────────────────────
ALLOWED_FILE_TYPES = ["pdf", "png", "jpg", "jpeg", "docx"]
MAX_FILE_SIZE_MB = 100
UPLOAD_FOLDER = "uploads"

# ──────────────────────────────────────────────
# Admin
# ──────────────────────────────────────────────
# Hardcoded demo admin — auto-created on startup so anyone can log in as admin.
# Demo/testing only; remove or change before any real deployment.
DEMO_ADMIN_EMAIL = "admin@novasbe.pt"
DEMO_ADMIN_PASSWORD = "admin123"
DEMO_ADMIN_USERNAME = "Admin"

ADMIN_EMAILS = [DEMO_ADMIN_EMAIL]  # these accounts get admin privileges on signup
