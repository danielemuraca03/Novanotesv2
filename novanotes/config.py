"""
NovaNotes — Shared configuration constants.
Edit these values to tune the platform behaviour.
"""

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
ADMIN_EMAILS = ["admin@novasbe.pt"]  # these accounts get admin privileges

# ──────────────────────────────────────────────
# Email verification
# ──────────────────────────────────────────────
VERIFICATION_TOKEN_EXPIRY_HOURS = 24
