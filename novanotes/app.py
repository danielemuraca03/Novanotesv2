"""
NovaNotes — Main entry point / Home page.
Run with: streamlit run app.py
"""

import streamlit as st
import db
import seed
from utils.style import get_custom_css
from utils.navbar import render_top_nav

st.set_page_config(
    page_title="NovaNotes",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

db.init_tables()
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
    # Hero banner
    st.markdown("""
    <div class="hero-banner">
        <h1>📚 NovaNotes</h1>
        <p>
            The study platform for <span class="hero-accent"><strong>Nova SBE students</strong></span>.<br>
            Share class notes, discover resources, and read honest course reviews.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Search box
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

    # How it works — feature cards
    st.markdown('<p class="home-search-label">How it works</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🎁", "20 free pts", "Awarded instantly on sign-up"),
        ("📤", "Earn 10 pts", "Every time you upload a note"),
        ("📥", "Spend 5 pts", "To download any document"),
        ("⭐", "Earn 2 pts", "When your notes are rated highly"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="fc-icon">{icon}</div>
                <div class="fc-title">{title}</div>
                <div class="fc-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👉 Click **Login** in the top nav to get started.")

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

    # Logged-in search shortcut
    st.markdown('<p class="home-search-label">🔍 Find notes</p>', unsafe_allow_html=True)
    with st.form("home_search_form_auth", clear_on_submit=False):
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

    # How it works — feature cards
    st.markdown('<p class="home-search-label">How it works</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🎁", "20 free pts", "Awarded instantly on sign-up"),
        ("📤", "Earn 10 pts", "Every time you upload a note"),
        ("📥", "Spend 5 pts", "To download any document"),
        ("⭐", "Earn 2 pts", "When your notes are rated highly"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="fc-icon">{icon}</div>
                <div class="fc-title">{title}</div>
                <div class="fc-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
