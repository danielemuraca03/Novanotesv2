"""
NovaNotes — Page 5: My Profile
"""

import html as html_lib
import streamlit as st
import db
from utils.style import get_custom_css
from utils.navbar import render_navbar

st.set_page_config(page_title="NovaNotes — Profile", page_icon="📚", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)
render_navbar()

# ── Login guard ──
if not st.session_state.get("user_id"):
    st.warning("Please log in to view your profile.")
    st.stop()

user = db.get_user_by_id(st.session_state.user_id)

# ── Profile header with avatar ──────────────────
initials = user["username"][0].upper() if user["username"] else "?"
username_esc = html_lib.escape(user["username"])
email_esc = html_lib.escape(user["email"])

st.markdown(f"""
<div class="profile-header">
    <div class="avatar-circle">{initials}</div>
    <div>
        <div style="font-size:20px;font-weight:700;color:#0d0d0d;margin-bottom:2px;">{username_esc}</div>
        <div style="font-size:13px;color:#888;">{email_esc}</div>
        <div style="font-size:12px;color:#bbb;margin-top:3px;">Member since {str(user['created_at'])[:10]}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats row ──────────────────────────────────
my_notes   = db.get_notes_by_user(st.session_state.user_id)
my_reviews = db.get_reviews_by_user(st.session_state.user_id)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Points balance", f"⭐ {user['points']}")
with col2:
    st.metric("Notes uploaded", len(my_notes))
with col3:
    st.metric("Reviews written", len(my_reviews))

st.divider()

# ── Tabs ──────────────────────────────────────
tab_notes, tab_reviews, tab_history, tab_leaderboard = st.tabs(
    ["My notes", "My reviews", "Points history", "Leaderboard"]
)

# ── My notes ──
with tab_notes:
    if not my_notes:
        st.info("You haven't uploaded any notes yet.")
    else:
        for note in my_notes:
            title_esc  = html_lib.escape(note["title"])
            course_esc = html_lib.escape(note["course"])
            prof_esc   = html_lib.escape(note["professor"])
            avg        = round(note["avg_rating"], 1)
            filled     = round(note["avg_rating"])
            stars_html = "★" * filled + "☆" * (5 - filled)

            st.markdown(f"""
            <div class="note-card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:15px;font-weight:600;color:#111;margin-bottom:2px;">{title_esc}</div>
                    <div style="font-size:13px;color:#777;">{course_esc} · Prof. {prof_esc}</div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:16px;">
                    <span class="stars-sm">{stars_html}</span>
                    <div style="font-size:12px;color:#aaa;">{avg} ({note['rating_count']})</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── My reviews ──
with tab_reviews:
    if not my_reviews:
        st.info("You haven't written any reviews yet.")
    else:
        for review in my_reviews:
            stars_html  = "★" * review["stars"] + "☆" * (5 - review["stars"])
            course_esc  = html_lib.escape(review["course"])
            prof_esc    = html_lib.escape(review["professor"])
            text_esc    = html_lib.escape(review["text"])
            sem_str     = f" · {html_lib.escape(review['semester'])}" if review.get("semester") else ""

            st.markdown(f"""
            <div class="review-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <div>
                        <span style="font-weight:600;color:#111;">{course_esc}</span>
                        <span style="color:#777;font-size:13px;"> · Prof. {prof_esc}</span>
                        <span style="color:#aaa;font-size:12px;">{sem_str}</span>
                    </div>
                    <span class="stars-sm" style="flex-shrink:0;">{stars_html}</span>
                </div>
                <p style="margin:0 0 6px;font-size:14px;color:#333;line-height:1.6;">{text_esc}</p>
                <p style="margin:0;font-size:12px;color:#bbb;">{str(review['created_at'])[:10]}</p>
            </div>
            """, unsafe_allow_html=True)

# ── Points history ──
with tab_history:
    history = db.get_points_history(st.session_state.user_id)
    if not history:
        st.info("No points activity yet.")
    else:
        rows_html = ""
        for entry in history:
            amount   = entry["amount"]
            sign     = "+" if amount > 0 else ""
            color    = "#00ab6b" if amount > 0 else "#e53935"
            reason   = html_lib.escape(entry["reason"])
            date_str = str(entry["created_at"])[:16]

            rows_html += f"""
            <div class="pts-row">
                <div>
                    <div style="font-size:14px;color:#222;margin-bottom:2px;">{reason}</div>
                    <div style="font-size:12px;color:#aaa;">{date_str}</div>
                </div>
                <span style="color:{color};font-weight:600;font-size:16px;flex-shrink:0;margin-left:16px;">
                    {sign}{amount}
                </span>
            </div>
            """
        st.markdown(f'<div style="background:white;border:1px solid #ebebeb;border-radius:8px;padding:8px 16px;">{rows_html}</div>', unsafe_allow_html=True)

# ── Leaderboard ──
with tab_leaderboard:
    st.markdown("### 🏆 Top contributors")
    leaders = db.get_leaderboard(limit=10)
    if not leaders:
        st.info("No users yet.")
    else:
        for i, leader in enumerate(leaders, 1):
            medal    = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            is_me    = leader["id"] == st.session_state.user_id
            me_class = " lb-me" if is_me else ""
            me_label = (
                " <span style='color:#00ab6b;font-weight:600;font-size:12px;'>← You</span>"
                if is_me else ""
            )
            uname_esc = html_lib.escape(leader["username"])

            st.markdown(f"""
            <div class="lb-row{me_class}">
                <span style="font-size:14px;color:#222;">
                    {medal}&nbsp; <strong>{uname_esc}</strong>{me_label}
                </span>
                <span class="points-badge" style="font-size:13px;padding:3px 12px;">
                    ⭐ {leader['points']}
                </span>
            </div>
            """, unsafe_allow_html=True)
