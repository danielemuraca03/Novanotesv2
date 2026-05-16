"""
NovaNotes — Database layer (Supabase PostgreSQL version).
Drop-in replacement for the SQLite db.py.
All SQL is here. Pages import functions, never write raw SQL.
"""

import psycopg2
import psycopg2.extras
import streamlit as st
from contextlib import contextmanager


# ──────────────────────────────────────────────
# Connection helper
# ──────────────────────────────────────────────
def _get_db_url():
    """Read the database URL from Streamlit secrets."""
    return st.secrets["DATABASE_URL"]


@contextmanager
def get_connection():
    """Yields a PostgreSQL connection with dict-like rows."""
    conn = psycopg2.connect(_get_db_url())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _query(sql, params=None, fetch="all"):
    """Helper: run a query and return results as list of dicts."""
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql, params or ())
        if fetch == "one":
            row = cur.fetchone()
            return dict(row) if row else None
        elif fetch == "all":
            return [dict(r) for r in cur.fetchall()]
        else:
            return None


def _execute(sql, params=None):
    """Helper: run an INSERT/UPDATE/DELETE and return lastrowid if applicable."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        try:
            row = cur.fetchone()
            return row[0] if row else None
        except psycopg2.ProgrammingError:
            return None


# ──────────────────────────────────────────────
# Table creation — not needed if you ran supabase_setup.sql,
# but kept here as a safety net on app startup.
# ──────────────────────────────────────────────
def init_tables():
    """Create all tables if they don't exist (PostgreSQL version)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            SERIAL PRIMARY KEY,
                email         TEXT   UNIQUE NOT NULL,
                username      TEXT   NOT NULL,
                password_hash TEXT   NOT NULL,
                is_admin      BOOLEAN DEFAULT FALSE,
                is_banned     BOOLEAN DEFAULT FALSE,
                points        INTEGER DEFAULT 0,
                created_at    TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS notes (
                id          SERIAL PRIMARY KEY,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                title       TEXT    NOT NULL,
                course      TEXT    NOT NULL,
                professor   TEXT    NOT NULL,
                year        INTEGER,
                description TEXT,
                file_path   TEXT    NOT NULL,
                file_type   TEXT    NOT NULL,
                is_removed  BOOLEAN DEFAULT FALSE,
                flagged     BOOLEAN DEFAULT FALSE,
                created_at  TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS ratings (
                id         SERIAL PRIMARY KEY,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                note_id    INTEGER NOT NULL REFERENCES notes(id),
                stars      INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                created_at TIMESTAMPTZ DEFAULT NOW(),
                UNIQUE(user_id, note_id)
            );

            CREATE TABLE IF NOT EXISTS reviews (
                id         SERIAL PRIMARY KEY,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                course     TEXT    NOT NULL,
                professor  TEXT    NOT NULL,
                semester   TEXT,
                text       TEXT    NOT NULL,
                stars      INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                is_removed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS points_log (
                id         SERIAL PRIMARY KEY,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                amount     INTEGER NOT NULL,
                reason     TEXT    NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS flags (
                id           SERIAL PRIMARY KEY,
                reporter_id  INTEGER NOT NULL REFERENCES users(id),
                content_type TEXT    NOT NULL,
                content_id   INTEGER NOT NULL,
                reason       TEXT    NOT NULL,
                resolved     BOOLEAN DEFAULT FALSE,
                created_at   TIMESTAMPTZ DEFAULT NOW()
            );
        """)


# ══════════════════════════════════════════════
#  USER functions
# ══════════════════════════════════════════════

def create_user(email, username, password_hash, initial_points=0, is_admin=False):
    """Insert a new user and return their id."""
    return _execute(
        """INSERT INTO users (email, username, password_hash, points, is_admin)
           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (email, username, password_hash, initial_points, is_admin),
    )


def get_user_by_email(email):
    """Return a user row by email, or None."""
    return _query(
        "SELECT * FROM users WHERE email = %s", (email,), fetch="one"
    )


def get_user_by_id(user_id):
    """Return a user row by id, or None."""
    return _query(
        "SELECT * FROM users WHERE id = %s", (user_id,), fetch="one"
    )


def ban_user(user_id):
    _execute("UPDATE users SET is_banned = TRUE WHERE id = %s", (user_id,))


def unban_user(user_id):
    _execute("UPDATE users SET is_banned = FALSE WHERE id = %s", (user_id,))


def get_all_users():
    return _query(
        """SELECT id, email, username, is_admin, is_banned, points, created_at
           FROM users ORDER BY created_at DESC"""
    )


# ══════════════════════════════════════════════
#  NOTE functions
# ══════════════════════════════════════════════

def save_note(user_id, title, course, professor, year, description, file_path, file_type):
    return _execute(
        """INSERT INTO notes (user_id, title, course, professor, year, description, file_path, file_type)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
        (user_id, title, course, professor, year, description, file_path, file_type),
    )


def get_notes(course=None, professor=None, search=None, sort_by="created_at"):
    query = """
        SELECT n.*, u.username,
               COALESCE(AVG(r.stars), 0) as avg_rating,
               COUNT(r.id) as rating_count
        FROM notes n
        JOIN users u ON n.user_id = u.id
        LEFT JOIN ratings r ON n.id = r.note_id
        WHERE n.is_removed = FALSE
    """
    params = []

    if course:
        query += " AND n.course = %s"
        params.append(course)
    if professor:
        query += " AND n.professor = %s"
        params.append(professor)
    if search:
        query += " AND (n.title ILIKE %s OR n.description ILIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " GROUP BY n.id, u.username"

    if sort_by == "rating":
        query += " ORDER BY avg_rating DESC"
    else:
        query += " ORDER BY n.created_at DESC"

    return _query(query, params)


def get_notes_by_user(user_id):
    return _query(
        """SELECT n.*, COALESCE(AVG(r.stars), 0) as avg_rating, COUNT(r.id) as rating_count
           FROM notes n
           LEFT JOIN ratings r ON n.id = r.note_id
           WHERE n.user_id = %s AND n.is_removed = FALSE
           GROUP BY n.id
           ORDER BY n.created_at DESC""",
        (user_id,),
    )


def remove_note(note_id):
    _execute("UPDATE notes SET is_removed = TRUE WHERE id = %s", (note_id,))


def get_all_notes_admin():
    return _query(
        """SELECT n.id, n.user_id, n.title, n.course, n.professor,
                  n.file_path, n.file_type, n.flagged, n.created_at,
                  u.username
           FROM notes n
           JOIN users u ON n.user_id = u.id
           WHERE n.is_removed = FALSE
           ORDER BY n.flagged DESC, n.created_at DESC"""
    )


def get_flagged_notes():
    return _query(
        """SELECT n.id, n.user_id, n.title, n.course, n.professor,
                  n.file_path, n.file_type, n.flagged, n.created_at,
                  u.username
           FROM notes n
           JOIN users u ON n.user_id = u.id
           WHERE n.is_removed = FALSE AND n.flagged = TRUE
           ORDER BY n.created_at DESC"""
    )


def set_note_flagged(note_id, flagged):
    _execute(
        "UPDATE notes SET flagged = %s WHERE id = %s",
        (flagged, note_id),
    )


def hard_delete_note(note_id):
    """Permanently delete a note: removes ratings, flags, and the note row.
    Returns the note row (with file_path, user_id, title) or None."""
    note = _query(
        "SELECT id, user_id, title, file_path FROM notes WHERE id = %s",
        (note_id,), fetch="one"
    )
    if note is None:
        return None
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM ratings WHERE note_id = %s", (note_id,))
        cur.execute(
            "DELETE FROM flags WHERE content_type = 'note' AND content_id = %s",
            (note_id,),
        )
        cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    return note


def get_all_courses():
    rows = _query(
        "SELECT DISTINCT course FROM notes WHERE is_removed = FALSE ORDER BY course"
    )
    return [row["course"] for row in rows]


def get_all_professors():
    rows = _query(
        "SELECT DISTINCT professor FROM notes WHERE is_removed = FALSE ORDER BY professor"
    )
    return [row["professor"] for row in rows]


# ══════════════════════════════════════════════
#  POINTS functions
# ══════════════════════════════════════════════

def award_points(user_id, amount, reason):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET points = points + %s WHERE id = %s",
            (amount, user_id),
        )
        cur.execute(
            "INSERT INTO points_log (user_id, amount, reason) VALUES (%s, %s, %s)",
            (user_id, amount, reason),
        )


def deduct_points(user_id, amount, reason):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT points FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        if row is None or row[0] < amount:
            return False
        cur.execute(
            "UPDATE users SET points = points - %s WHERE id = %s",
            (amount, user_id),
        )
        cur.execute(
            "INSERT INTO points_log (user_id, amount, reason) VALUES (%s, %s, %s)",
            (user_id, -amount, reason),
        )
        return True


def revert_upload_points(user_id, amount, reason):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT points FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        if row is None:
            return
        deducted = min(row[0], amount)
        cur.execute(
            "UPDATE users SET points = points - %s WHERE id = %s",
            (deducted, user_id),
        )
        cur.execute(
            "INSERT INTO points_log (user_id, amount, reason) VALUES (%s, %s, %s)",
            (user_id, -amount, reason),
        )


def get_points_balance(user_id):
    row = _query(
        "SELECT points FROM users WHERE id = %s", (user_id,), fetch="one"
    )
    return row["points"] if row else 0


def get_points_history(user_id):
    return _query(
        "SELECT * FROM points_log WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )


def get_leaderboard(limit=10):
    return _query(
        """SELECT id, username, points
           FROM users
           WHERE is_banned = FALSE
           ORDER BY points DESC
           LIMIT %s""",
        (limit,),
    )


# ══════════════════════════════════════════════
#  RATING functions
# ══════════════════════════════════════════════

def add_rating(user_id, note_id, stars):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO ratings (user_id, note_id, stars)
               VALUES (%s, %s, %s)
               ON CONFLICT(user_id, note_id)
               DO UPDATE SET stars = EXCLUDED.stars""",
            (user_id, note_id, stars),
        )


def get_user_rating(user_id, note_id):
    row = _query(
        "SELECT stars FROM ratings WHERE user_id = %s AND note_id = %s",
        (user_id, note_id), fetch="one"
    )
    return row["stars"] if row else None


def get_ratings_by_user(user_id):
    return _query(
        """SELECT r.stars, r.created_at,
                  n.id as note_id, n.title, n.course, n.professor
           FROM ratings r
           JOIN notes n ON r.note_id = n.id
           WHERE r.user_id = %s AND n.is_removed = FALSE
           ORDER BY r.created_at DESC""",
        (user_id,),
    )


# ══════════════════════════════════════════════
#  REVIEW functions
# ══════════════════════════════════════════════

def create_review(user_id, course, professor, semester, text, stars):
    return _execute(
        """INSERT INTO reviews (user_id, course, professor, semester, text, stars)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (user_id, course, professor, semester, text, stars),
    )


def get_reviews(course=None, professor=None):
    query = """
        SELECT rv.*, u.username
        FROM reviews rv
        JOIN users u ON rv.user_id = u.id
        WHERE rv.is_removed = FALSE
    """
    params = []
    if course:
        query += " AND rv.course = %s"
        params.append(course)
    if professor:
        query += " AND rv.professor = %s"
        params.append(professor)
    query += " ORDER BY rv.created_at DESC"
    return _query(query, params)


def get_reviews_by_user(user_id):
    return _query(
        "SELECT * FROM reviews WHERE user_id = %s AND is_removed = FALSE ORDER BY created_at DESC",
        (user_id,),
    )


def remove_review(review_id):
    _execute("UPDATE reviews SET is_removed = TRUE WHERE id = %s", (review_id,))


# ══════════════════════════════════════════════
#  FLAG functions
# ══════════════════════════════════════════════

def create_flag(reporter_id, content_type, content_id, reason):
    _execute(
        """INSERT INTO flags (reporter_id, content_type, content_id, reason)
           VALUES (%s, %s, %s, %s)""",
        (reporter_id, content_type, content_id, reason),
    )


def get_pending_flags():
    return _query(
        """SELECT f.*, u.username as reporter_name
           FROM flags f
           JOIN users u ON f.reporter_id = u.id
           WHERE f.resolved = FALSE
           ORDER BY f.created_at DESC"""
    )


def resolve_flag(flag_id):
    _execute("UPDATE flags SET resolved = TRUE WHERE id = %s", (flag_id,))


# ══════════════════════════════════════════════
#  STATS functions
# ══════════════════════════════════════════════

def get_stats():
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT COUNT(*) as c FROM users")
        total_users = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM notes WHERE is_removed = FALSE")
        total_notes = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM reviews WHERE is_removed = FALSE")
        total_reviews = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM points_log WHERE reason LIKE 'Downloaded: %%'")
        total_downloads = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM flags WHERE resolved = FALSE")
        pending_flags = cur.fetchone()["c"]
        return {
            "total_users": total_users,
            "total_notes": total_notes,
            "total_reviews": total_reviews,
            "total_downloads": total_downloads,
            "pending_flags": pending_flags,
        }
