"""
NovaNotes — Demo data seeder.
Runs once on startup when the notes table is empty.
Add files to seed_data/files/ and entries to seed_data/manifest.json
to include them as permanent demo content.
"""

import json
import os
import shutil

import db
from config import UPLOAD_FOLDER

SEED_DIR = os.path.join(os.path.dirname(__file__), "seed_data")
SEED_FILES_DIR = os.path.join(SEED_DIR, "manifest.json")
SEED_USER_EMAIL = "seed@novanotes.internal"


def _get_or_create_seed_user():
    user = db.get_user_by_email(SEED_USER_EMAIL)
    if user:
        return user["id"]
    import bcrypt
    pw_hash = bcrypt.hashpw(b"seed-internal", bcrypt.gensalt()).decode()
    user_id = db.create_user(
        email=SEED_USER_EMAIL,
        username="NovaNotes Team",
        password_hash=pw_hash,
        initial_points=0,
        is_admin=False,
    )
    db.verify_user(user_id)
    return user_id


def seed_demo_notes():
    """Load demo notes from seed_data/ if the notes table is empty."""
    import sqlite3
    with db.get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) as c FROM notes").fetchone()["c"]
    if count > 0:
        return

    manifest_path = os.path.join(SEED_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        return

    with open(manifest_path, encoding="utf-8") as f:
        entries = json.load(f)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    user_id = _get_or_create_seed_user()

    for entry in entries:
        src = os.path.join(SEED_DIR, "files", entry["file"])
        if not os.path.exists(src):
            continue

        ext = entry["file"].rsplit(".", 1)[-1].lower()
        dest_name = f"seed_{entry['file']}"
        dest = os.path.join(UPLOAD_FOLDER, dest_name)
        shutil.copy2(src, dest)

        db.save_note(
            user_id=user_id,
            title=entry["title"],
            course=entry["course"],
            professor=entry["professor"],
            year=entry.get("year"),
            description=entry.get("description", ""),
            file_path=dest,
            file_type=ext,
        )
