"""
NovaNotes — Page 5: My Profile
(Pair 2 builds this page)
"""

import streamlit as st
import db
from utils.style import get_custom_css

st.set_page_config(page_title="NovaNotes — Profile", page_icon="📚", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── Login guard ──
if not st.session_state.get("user_id"):
    st.warning("Please log in to view your profile.")
    st.stop()

user = db.get_user_by_id(st.session_state.user_id)

st.markdown(f"# 👤 {user['username']}")
st.caption(f"{user['email']} · Joined {str(user['created_at'])[:10]}")

# ── Stats row ──
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Points balance", f"⭐ {user['points']}")
with col2:
    my_notes = db.get_notes_by_user(st.session_state.user_id)
    st.metric("Notes uploaded", len(my_notes))
with col3:
    my_reviews = db.get_reviews_by_user(st.session_state.user_id)
    st.metric("Reviews written", len(my_reviews))

st.divider()

# ── Tabs ──
tab_notes, tab_reviews, tab_history, tab_leaderboard = st.tabs(
    ["My notes", "My reviews", "Points history", "Leaderboard"]
)

# ── My notes ──
with tab_notes:
    if not my_notes:
        st.info("You haven't uploaded any notes yet.")
    else:
        for note in my_notes:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{note['title']}**")
                st.caption(f"{note['course']} · Prof. {note['professor']}")
            with col2:
                avg = round(note["avg_rating"], 1)
                st.markdown(f"⭐ {avg} ({note['rating_count']})")
            st.divider()

# ── My reviews ──
with tab_reviews:
    if not my_reviews:
        st.info("You haven't written any reviews yet.")
    else:
        for review in my_reviews:
            stars = "★" * review["stars"] + "☆" * (5 - review["stars"])
            st.markdown(f"**{review['course']}** · Prof. {review['professor']}")
            st.markdown(f'<span class="stars">{stars}</span>', unsafe_allow_html=True)
            st.write(review["text"])
            st.caption(str(review["created_at"])[:10])
            st.divider()

# ── Points history ──
with tab_history:
    history = db.get_points_history(st.session_state.user_id)
    if not history:
        st.info("No points activity yet.")
    else:
        for entry in history:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(entry["reason"])
                st.caption(str(entry["created_at"])[:16])
            with col2:
                amount = entry["amount"]
                color = "green" if amount > 0 else "red"
                sign = "+" if amount > 0 else ""
                st.markdown(
                    f'<span style="color:{color}; font-weight:500; font-size:16px;">'
                    f'{sign}{amount}</span>',
                    unsafe_allow_html=True,
                )
            st.divider()

# ── Leaderboard ──
with tab_leaderboard:
    st.markdown("### 🏆 Top contributors")
    leaders = db.get_leaderboard(limit=10)
    if not leaders:
        st.info("No users yet.")
    else:
        for i, leader in enumerate(leaders, 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
                highlight = " **← You!**" if leader["id"] == st.session_state.user_id else ""
                st.markdown(f"{medal} **{leader['username']}**{highlight}")
            with col2:
                st.markdown(f"⭐ {leader['points']}")
            st.divider()
