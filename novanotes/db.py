"""
NovaNotes — Database layer.
All SQL lives here. Pages import functions, never write raw SQL.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

DB_PATH = "novanotes.db"


# ──────────────────────────────────────────────
# Connection helper
# ──────────────────────────────────────────────
@contextmanager
def get_connection():
    """Yields a SQLite connection with row_factory set to sqlite3.Row."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ──────────────────────────────────────────────
# Table creation (run once on startup)
# ──────────────────────────────────────────────
def init_tables():
    """Create all tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT    UNIQUE NOT NULL,
                username      TEXT    NOT NULL,
                password_hash TEXT    NOT NULL,
                is_verified   BOOLEAN DEFAULT 0,
                is_admin      BOOLEAN DEFAULT 0,
                is_banned     BOOLEAN DEFAULT 0,
                points        INTEGER DEFAULT 0,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS verification_tokens (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                token      TEXT    UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used       BOOLEAN DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS notes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                title       TEXT    NOT NULL,
                course      TEXT    NOT NULL,
                professor   TEXT    NOT NULL,
                year        INTEGER,
                description TEXT,
                file_path   TEXT    NOT NULL,
                file_type   TEXT    NOT NULL,
                is_removed  BOOLEAN DEFAULT 0,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS ratings (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                note_id    INTEGER NOT NULL REFERENCES notes(id),
                stars      INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, note_id)
            );

            CREATE TABLE IF NOT EXISTS reviews (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                course     TEXT    NOT NULL,
                professor  TEXT    NOT NULL,
                semester   TEXT,
                text       TEXT    NOT NULL,
                stars      INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                is_removed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS points_log (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                amount     INTEGER NOT NULL,
                reason     TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS flags (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_id  INTEGER NOT NULL REFERENCES users(id),
                content_type TEXT    NOT NULL,
                content_id   INTEGER NOT NULL,
                reason       TEXT    NOT NULL,
                resolved     BOOLEAN DEFAULT 0,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)


# ══════════════════════════════════════════════
#  USER functions  
# ══════════════════════════════════════════════

def create_user(email, username, password_hash, initial_points=0, is_admin=False):
    """Insert a new user and return their id."""
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO users (email, username, password_hash, points, is_admin)
               VALUES (?, ?, ?, ?, ?)""",
            (email, username, password_hash, initial_points, is_admin),
        )
        return cursor.lastrowid


def get_user_by_email(email):
    """Return a user row by email, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()


def get_user_by_id(user_id):
    """Return a user row by id, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


def verify_user(user_id):
    """Mark a user as email-verified."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET is_verified = 1 WHERE id = ?", (user_id,)
        )


def ban_user(user_id):
    """Ban a user account."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET is_banned = 1 WHERE id = ?", (user_id,)
        )


def unban_user(user_id):
    """Unban a user account."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET is_banned = 0 WHERE id = ?", (user_id,)
        )


def get_all_users():
    """Return all users (for admin panel)."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, email, username, is_verified, is_admin, is_banned, points, created_at FROM users ORDER BY created_at DESC"
        ).fetchall()


# ══════════════════════════════════════════════
#  VERIFICATION TOKEN functions
# ══════════════════════════════════════════════

def create_verification_token(user_id, token, expiry_hours=24):
    """Store a verification token for a user."""
    expires_at = datetime.now() + timedelta(hours=expiry_hours)
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO verification_tokens (user_id, token, expires_at)
               VALUES (?, ?, ?)""",
            (user_id, token, expires_at),
        )


def get_verification_token(token):
    """Return token row if valid (not used, not expired)."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT * FROM verification_tokens
               WHERE token = ? AND used = 0 AND expires_at > ?""",
            (token, datetime.now()),
        ).fetchone()


def mark_token_used(token):
    """Mark a verification token as used."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE verification_tokens SET used = 1 WHERE token = ?", (token,)
        )


# ══════════════════════════════════════════════
#  NOTE functions  
# ══════════════════════════════════════════════

def save_note(user_id, title, course, professor, year, description, file_path, file_type):
    """Insert a new note and return its id."""
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO notes (user_id, title, course, professor, year, description, file_path, file_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, title, course, professor, year, description, file_path, file_type),
        )
        return cursor.lastrowid


def get_notes(course=None, professor=None, search=None, sort_by="created_at"):
    """Return notes matching filters. Only non-removed notes."""
    query = """
        SELECT n.*, u.username,
               COALESCE(AVG(r.stars), 0) as avg_rating,
               COUNT(r.id) as rating_count
        FROM notes n
        JOIN users u ON n.user_id = u.id
        LEFT JOIN ratings r ON n.id = r.note_id
        WHERE n.is_removed = 0
    """
    params = []

    if course:
        query += " AND n.course = ?"
        params.append(course)
    if professor:
        query += " AND n.professor = ?"
        params.append(professor)
    if search:
        query += " AND (n.title LIKE ? OR n.description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " GROUP BY n.id"

    if sort_by == "rating":
        query += " ORDER BY avg_rating DESC"
    else:
        query += " ORDER BY n.created_at DESC"

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def get_note_by_id(note_id):
    """Return a single note with uploader info and avg rating."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT n.*, u.username,
                      COALESCE(AVG(r.stars), 0) as avg_rating,
                      COUNT(r.id) as rating_count
               FROM notes n
               JOIN users u ON n.user_id = u.id
               LEFT JOIN ratings r ON n.id = r.note_id
               WHERE n.id = ?
               GROUP BY n.id""",
            (note_id,),
        ).fetchone()


def get_notes_by_user(user_id):
    """Return all notes uploaded by a specific user."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT n.*, COALESCE(AVG(r.stars), 0) as avg_rating, COUNT(r.id) as rating_count
               FROM notes n
               LEFT JOIN ratings r ON n.id = r.note_id
               WHERE n.user_id = ? AND n.is_removed = 0
               GROUP BY n.id
               ORDER BY n.created_at DESC""",
            (user_id,),
        ).fetchall()


def remove_note(note_id):
    """Soft-delete a note (admin action)."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE notes SET is_removed = 1 WHERE id = ?", (note_id,)
        )


def get_all_courses():
    """Return distinct course names for filter dropdowns."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT course FROM notes WHERE is_removed = 0 ORDER BY course"
        ).fetchall()
        return [row["course"] for row in rows]


def get_all_professors():
    """Return distinct professor names for filter dropdowns."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT professor FROM notes WHERE is_removed = 0 ORDER BY professor"
        ).fetchall()
        return [row["professor"] for row in rows]


# ══════════════════════════════════════════════
#  POINTS functions  
# ══════════════════════════════════════════════

def award_points(user_id, amount, reason):
    """Add points to a user and log the transaction."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET points = points + ? WHERE id = ?",
            (amount, user_id),
        )
        conn.execute(
            "INSERT INTO points_log (user_id, amount, reason) VALUES (?, ?, ?)",
            (user_id, amount, reason),
        )


def deduct_points(user_id, amount, reason):
    """Remove points from a user and log the transaction. Returns False if insufficient."""
    with get_connection() as conn:
        user = conn.execute(
            "SELECT points FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if user is None or user["points"] < amount:
            return False
        conn.execute(
            "UPDATE users SET points = points - ? WHERE id = ?",
            (amount, user_id),
        )
        conn.execute(
            "INSERT INTO points_log (user_id, amount, reason) VALUES (?, ?, ?)",
            (user_id, -amount, reason),
        )
        return True


def get_points_balance(user_id):
    """Return current points balance."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT points FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return row["points"] if row else 0


def get_points_history(user_id):
    """Return full points transaction log for a user."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM points_log WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()


def get_leaderboard(limit=10):
    """Return top users by points."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT id, username, points
               FROM users
               WHERE is_banned = 0
               ORDER BY points DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()


# ══════════════════════════════════════════════
#  RATING functions  (Pair 2 builds these)
# ══════════════════════════════════════════════

def add_rating(user_id, note_id, stars):
    """Upsert a star rating (one per user per note)."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO ratings (user_id, note_id, stars)
               VALUES (?, ?, ?)
               ON CONFLICT(user_id, note_id)
               DO UPDATE SET stars = excluded.stars""",
            (user_id, note_id, stars),
        )


def get_user_rating(user_id, note_id):
    """Return the user's existing rating for a note, or None."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT stars FROM ratings WHERE user_id = ? AND note_id = ?",
            (user_id, note_id),
        ).fetchone()
        return row["stars"] if row else None


def get_ratings_by_user(user_id):
    """Return all ratings given by a user, joined with note details."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT r.stars, r.created_at,
                      n.id as note_id, n.title, n.course, n.professor
               FROM ratings r
               JOIN notes n ON r.note_id = n.id
               WHERE r.user_id = ? AND n.is_removed = 0
               ORDER BY r.created_at DESC""",
            (user_id,),
        ).fetchall()


# ══════════════════════════════════════════════
#  REVIEW functions  
# ══════════════════════════════════════════════

def create_review(user_id, course, professor, semester, text, stars):
    """Insert a new course/teacher review."""
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO reviews (user_id, course, professor, semester, text, stars)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, course, professor, semester, text, stars),
        )
        return cursor.lastrowid


def get_reviews(course=None, professor=None):
    """Return reviews matching filters."""
    query = """
        SELECT rv.*, u.username
        FROM reviews rv
        JOIN users u ON rv.user_id = u.id
        WHERE rv.is_removed = 0
    """
    params = []
    if course:
        query += " AND rv.course = ?"
        params.append(course)
    if professor:
        query += " AND rv.professor = ?"
        params.append(professor)
    query += " ORDER BY rv.created_at DESC"

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def get_reviews_by_user(user_id):
    """Return all reviews by a specific user."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM reviews WHERE user_id = ? AND is_removed = 0 ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()


def remove_review(review_id):
    """Soft-delete a review (admin action)."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE reviews SET is_removed = 1 WHERE id = ?", (review_id,)
        )


# ══════════════════════════════════════════════
#  FLAG functions  
# ══════════════════════════════════════════════

def create_flag(reporter_id, content_type, content_id, reason):
    """Flag a note or review for moderation."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO flags (reporter_id, content_type, content_id, reason)
               VALUES (?, ?, ?, ?)""",
            (reporter_id, content_type, content_id, reason),
        )


def get_pending_flags():
    """Return all unresolved flags."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT f.*, u.username as reporter_name
               FROM flags f
               JOIN users u ON f.reporter_id = u.id
               WHERE f.resolved = 0
               ORDER BY f.created_at DESC"""
        ).fetchall()


def resolve_flag(flag_id):
    """Mark a flag as resolved."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE flags SET resolved = 1 WHERE id = ?", (flag_id,)
        )


# ══════════════════════════════════════════════
#  STATS functions 
# ══════════════════════════════════════════════

def get_stats():
    """Return platform-wide statistics."""
    with get_connection() as conn:
        total_users = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        total_notes = conn.execute("SELECT COUNT(*) as c FROM notes WHERE is_removed = 0").fetchone()["c"]
        total_reviews = conn.execute("SELECT COUNT(*) as c FROM reviews WHERE is_removed = 0").fetchone()["c"]
        total_downloads = conn.execute(
            "SELECT COUNT(*) as c FROM points_log WHERE reason LIKE '%download%'"
        ).fetchone()["c"]
        pending_flags = conn.execute(
            "SELECT COUNT(*) as c FROM flags WHERE resolved = 0"
        ).fetchone()["c"]
        return {
            "total_users": total_users,
            "total_notes": total_notes,
            "total_reviews": total_reviews,
            "total_downloads": total_downloads,
            "pending_flags": pending_flags,
        }
