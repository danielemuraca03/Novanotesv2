"""
NovaNotes — Page 4: Course & Teacher Reviews
(Pair 2 builds this page)
"""

import streamlit as st
import db
from utils.style import get_custom_css

st.set_page_config(page_title="NovaNotes — Reviews", page_icon="📚", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown("# ⭐ Course & teacher reviews")

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

    if not reviews:
        st.info("No reviews yet. Be the first to write one!")
    else:
        for review in reviews:
            stars_display = "★" * review["stars"] + "☆" * (5 - review["stars"])
            with st.container():
                st.markdown(
                    f"""<div class="note-card">
                        <div style="display:flex; justify-content:space-between;">
                            <div>
                                <strong>{review["course"]}</strong> · Prof. {review["professor"]}
                                <span style="color:#999; font-size:12px;"> · {review["semester"] or ""}</span>
                            </div>
                            <span class="stars">{stars_display}</span>
                        </div>
                        <p style="margin:8px 0 4px; font-size:14px;">{review["text"]}</p>
                        <p style="color:#999; font-size:12px; margin:0;">
                            by {review["username"]} · {str(review["created_at"])[:10]}
                        </p>
                    </div>""",
                    unsafe_allow_html=True,
                )

                # ── Flag button ──
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
        st.stop()

    with st.form("review_form"):
        rev_course = st.text_input("Course *", placeholder="e.g. Microeconomics I")
        rev_professor = st.text_input("Professor *", placeholder="e.g. Prof. Santos")
        rev_semester = st.text_input("Semester", placeholder="e.g. Fall 2025")
        rev_stars = st.slider("Rating", min_value=1, max_value=5, value=3)
        rev_text = st.text_area(
            "Your review *",
            placeholder="Share your experience with this course and professor...",
            max_chars=1000,
        )
        submitted = st.form_submit_button("Submit review", use_container_width=True)

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
            st.success("Review published! Thank you for sharing.")
            st.rerun()
