"""
NovaNotes — Main entry point.
Run with: streamlit run app.py
"""

import streamlit as st
import db
import seed
from utils.style import get_custom_css
from utils.email_verify import handle_verification
from config import ADMIN_EMAILS

# ──────────────────────────────────────────────
# Page config (must be first Streamlit command)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="NovaNotes",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Inject custom CSS
# ──────────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Initialise database on first run
# ──────────────────────────────────────────────
db.init_tables()
seed.seed_demo_notes()

# ──────────────────────────────────────────────
# Handle email verification tokens in URL
# ──────────────────────────────────────────────
handle_verification()

# ──────────────────────────────────────────────
# Session state defaults
# ──────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False
    st.session_state.points = 0

# ──────────────────────────────────────────────
# Sidebar: user info + logout
# ──────────────────────────────────────────────
with st.sidebar:
    st.title("📚 NovaNotes")
    st.caption("Share knowledge, earn points")
    st.divider()

    if st.session_state.user_id:
        st.markdown(f"👋 **{st.session_state.username}**")

        # Refresh points from DB
        st.session_state.points = db.get_points_balance(st.session_state.user_id)
        st.markdown(
            f'<span class="points-badge">⭐ {st.session_state.points} points</span>',
            unsafe_allow_html=True,
        )
        st.divider()

        if st.button("🚪 Log out", use_container_width=True):
            for key in ["user_id", "username", "is_admin", "points"]:
                st.session_state[key] = None if key != "points" else 0
            st.session_state.is_admin = False
            st.rerun()
    else:
        st.info("Log in to upload and download notes.")


# ──────────────────────────────────────────────
# Main content area (landing page)
# ──────────────────────────────────────────────
if st.session_state.user_id is None:
    st.markdown("# Welcome to NovaNotes 📚")
    st.markdown(
        """
        The platform where **Nova SBE students** share class notes,
        study tips, and course reviews.

        **How it works:**
        - 🎁 Get **20 free points** when you sign up
        - 📤 **Earn 10 points** for every note you upload
        - 📥 **Spend 5 points** to download a note
        - ⭐ **Earn 2 points** when someone rates your note highly

        👉 Head to the **Login** page in the sidebar to get started.
        """
    )
else:
    st.markdown(f"# Welcome back, {st.session_state.username}! 👋")

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your points", f"⭐ {st.session_state.points}")
    with col2:
        my_notes = db.get_notes_by_user(st.session_state.user_id)
        st.metric("Notes uploaded", len(my_notes))
    with col3:
        my_reviews = db.get_reviews_by_user(st.session_state.user_id)
        st.metric("Reviews written", len(my_reviews))

    st.divider()
    st.markdown("Use the **sidebar** to navigate to Browse, Upload, Reviews, or your Profile.")
