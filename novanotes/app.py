"""
NovaNotes — Main entry point / Home page.
Run with: streamlit run app.py
"""

import bcrypt
import streamlit as st
import db
import seed
from config import DEMO_ADMIN_EMAIL, DEMO_ADMIN_PASSWORD, DEMO_ADMIN_USERNAME
from utils.style import get_custom_css
from utils.navbar import render_top_nav


def _ensure_demo_admin():
    """Auto-create (or upgrade) the hardcoded demo admin account on startup."""
    existing = db.get_user_by_email(DEMO_ADMIN_EMAIL)
    pw_hash = bcrypt.hashpw(DEMO_ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
    if existing is None:
        db.create_user(
            email=DEMO_ADMIN_EMAIL,
            username=DEMO_ADMIN_USERNAME,
            password_hash=pw_hash,
            initial_points=0,
            is_admin=True,
        )
    else:
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ?, is_admin = 1, is_banned = 0 WHERE email = ?",
                (pw_hash, DEMO_ADMIN_EMAIL),
            )

st.set_page_config(
    page_title="NovaNotes",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

db.init_tables()
_ensure_demo_admin()
seed.seed_demo_notes()

if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False
    st.session_state.points = 0

if st.session_state.user_id:
    st.session_state.points = db.get_points_balance(st.session_state.user_id)

# ── Top navbar ───────────────────────────────────
render_top_nav("Home")

# ── Main content ──────────────────────────────────
if st.session_state.user_id is None:
    st.markdown("""
    <div class="hero-banner">
        <h1>📚 NovaNotes</h1>
        <p>
            The study platform for <span class="hero-accent"><strong>Nova SBE students</strong></span>.<br>
            Share class notes, discover resources, and read honest course reviews.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"## Welcome back, {st.session_state.username}! 👋")
    st.caption("Here's a snapshot of your activity.")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Points balance", f"⭐ {st.session_state.points}")
    with col2:
        my_notes = db.get_notes_by_user(st.session_state.user_id)
        st.metric("Notes uploaded", len(my_notes))
    with col3:
        my_reviews = db.get_reviews_by_user(st.session_state.user_id)
        st.metric("Reviews written", len(my_reviews))

    st.divider()

# ── Search box (shared) ────────────────────────────
st.markdown('<p class="home-search-label">🔍 Find notes</p>', unsafe_allow_html=True)
with st.form("home_search_form", clear_on_submit=False):
    col_s, col_b = st.columns([5, 1])
    with col_s:
        home_search = st.text_input(
            "Search",
            placeholder="Search for notes, courses, professors...",
            label_visibility="collapsed",
        )
    with col_b:
        search_submitted = st.form_submit_button("Search", use_container_width=True)

if search_submitted:
    if home_search.strip():
        st.session_state["home_search"] = home_search.strip()
    st.switch_page("pages/2_Browse.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── How it works — feature cards (shared) ──────────
st.markdown('<p class="home-search-label">How it works</p>', unsafe_allow_html=True)
cols = st.columns(4)
features = [
    ("🎁", "20 free pts", "Awarded instantly on sign-up"),
    ("📤", "Earn 10 pts", "Every time you upload a note"),
    ("📥", "Spend 5 pts", "To download any document"),
    ("⭐", "Earn 2 pts", "When your notes are rated highly"),
]
for col, (icon, title, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="fc-icon">{icon}</div>
            <div class="fc-title">{title}</div>
            <div class="fc-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.user_id is None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👉 Click **Login** in the top nav to get started.")
