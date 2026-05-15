"""
NovaNotes — Page 4: Course & Teacher Reviews
"""

import html as html_lib
import streamlit as st
import db
from utils.style import get_custom_css
from utils.navbar import render_top_nav

st.set_page_config(page_title="NovaNotes — Reviews", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
st.markdown(get_custom_css(), unsafe_allow_html=True)
render_top_nav("Reviews")

st.markdown("# ⭐ Course & teacher reviews")

if st.session_state.pop("review_publish_success", False):
    st.success("Review published! Thank you for sharing.")

tab_browse, tab_write = st.tabs(["Browse reviews", "Write a review"])

# ══════════════════════════════════════════════
#  BROWSE REVIEWS
# ══════════════════════════════════════════════
with tab_browse:
    col1, col2 = st.columns(2)
    with col1:
        filter_course = st.text_input("Filter by course", placeholder="e.g. Finance I")
    with col2:
        filter_prof = st.text_input("Filter by professor", placeholder="e.g. Prof. Santos")

    reviews = db.get_reviews(
        course=filter_course if filter_course else None,
        professor=filter_prof if filter_prof else None,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not reviews:
        st.info("No reviews yet. Be the first to write one!")
    else:
        for review in reviews:
            stars_filled = "★" * review["stars"] + "☆" * (5 - review["stars"])
            course_esc   = html_lib.escape(review["course"])
            prof_esc     = html_lib.escape(review["professor"])
            text_esc     = html_lib.escape(review["text"])
            uname_esc    = html_lib.escape(review["username"])
            sem_str      = f" · {html_lib.escape(review['semester'])}" if review['semester'] else ""
            date_str     = str(review["created_at"])[:10]

            st.markdown(f"""
            <div class="review-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div>
                        <span style="font-size:15px;font-weight:600;color:#111;">{course_esc}</span>
                        <span style="font-size:13px;color:#777;"> · Prof. {prof_esc}</span>
                        <span style="font-size:12px;color:#aaa;">{sem_str}</span>
                    </div>
                    <span class="stars-sm" style="flex-shrink:0;margin-left:12px;">{stars_filled}</span>
                </div>
                <p style="margin:0 0 10px;font-size:14px;color:#333;line-height:1.65;">{text_esc}</p>
                <p style="margin:0;font-size:12px;color:#aaa;">by {uname_esc} · {date_str}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.get("user_id") and review["user_id"] != st.session_state.user_id:
                if st.button("🚩 Flag", key=f"flag_review_{review['id']}"):
                    db.create_flag(
                        st.session_state.user_id,
                        "review",
                        review["id"],
                        "Flagged by user",
                    )
                    st.warning("Review flagged for moderation.")

# ══════════════════════════════════════════════
#  WRITE A REVIEW
# ══════════════════════════════════════════════
with tab_write:
    if not st.session_state.get("user_id"):
        st.warning("Please log in to write a review.")
        if st.button("Go to login", type="primary", key="reviews_go_login"):
            st.switch_page("pages/1_Login.py")
        st.stop()

    with st.form("review_form"):
        rev_course    = st.text_input("Course *", placeholder="e.g. Microeconomics I")
        rev_professor = st.text_input("Professor *", placeholder="e.g. Prof. Santos")
        rev_semester  = st.text_input("Semester", placeholder="e.g. Fall 2025")
        rev_stars     = st.slider("Rating", min_value=1, max_value=5, value=3)
        rev_text      = st.text_area(
            "Your review *",
            placeholder="Share your experience with this course and professor...",
            max_chars=1000,
        )
        submitted = st.form_submit_button("Publish review", use_container_width=True)

    if submitted:
        if not rev_course or not rev_professor or not rev_text:
            st.error("Please fill in all required fields.")
        else:
            db.create_review(
                user_id=st.session_state.user_id,
                course=rev_course.strip(),
                professor=rev_professor.strip(),
                semester=rev_semester.strip() if rev_semester else "",
                text=rev_text.strip(),
                stars=rev_stars,
            )
            st.session_state["review_publish_success"] = True
            st.rerun()
