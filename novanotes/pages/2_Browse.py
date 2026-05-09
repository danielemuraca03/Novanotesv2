"""
NovaNotes — Page 2: Browse Notes
"""

import streamlit as st
import db
from config import POINTS_PER_DOWNLOAD
from utils.style import get_custom_css

st.set_page_config(page_title="NovaNotes — Browse", page_icon="📚", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown("# 📖 Browse notes")

# ── Filters ──
col_search, col_course, col_prof, col_sort = st.columns([2, 1.5, 1.5, 1])

with col_search:
    search_query = st.text_input("🔍 Search", placeholder="e.g. microeconomics midterm", label_visibility="collapsed")

courses = ["All"] + db.get_all_courses()
professors = ["All"] + db.get_all_professors()

with col_course:
    selected_course = st.selectbox("Course", courses, label_visibility="collapsed")

with col_prof:
    selected_prof = st.selectbox("Professor", professors, label_visibility="collapsed")

with col_sort:
    sort_by = st.selectbox("Sort", ["Newest", "Top rated"], label_visibility="collapsed")

# ── Fetch notes ──
notes = db.get_notes(
    course=selected_course if selected_course != "All" else None,
    professor=selected_prof if selected_prof != "All" else None,
    search=search_query if search_query else None,
    sort_by="rating" if sort_by == "Top rated" else "created_at",
)

if not notes:
    st.info("No notes found. Try adjusting your filters or be the first to upload!")
    st.stop()

st.caption(f"{len(notes)} note{'s' if len(notes) != 1 else ''} found")


# ── Helper: render stars ──
def render_stars(avg, count):
    filled = round(avg)
    stars_html = "★" * filled + "☆" * (5 - filled)
    return f'<span class="stars">{stars_html}</span> <span style="color:#999; font-size:13px;">({count})</span>'


# ── Display note cards ──
for note in notes:
    with st.container():
        st.markdown(
            f"""<div class="note-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h3 style="margin:0 0 4px; font-size:17px;">{note["title"]}</h3>
                        <p style="color:#666; margin:0; font-size:13px;">
                            {note["course"]} · Prof. {note["professor"]} · {note["year"] or ""}
                        </p>
                    </div>
                    <div style="text-align:right;">
                        {render_stars(note["avg_rating"], note["rating_count"])}
                        <p style="color:#999; font-size:12px; margin:4px 0 0;">
                            by {note["username"]} · {str(note["created_at"])[:10]}
                        </p>
                    </div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

        # Description + download in expander
        with st.expander("View details"):
            if note["description"]:
                st.write(note["description"])

            st.markdown(f"**File type:** {note['file_type'].upper()}")
            st.markdown(f"**Cost:** {POINTS_PER_DOWNLOAD} points")

            # ── Download logic ──
            if not st.session_state.get("user_id"):
                st.warning("Log in to download this note.")
            elif note["user_id"] == st.session_state.user_id:
                # Own note — free download
                try:
                    with open(note["file_path"], "rb") as f:
                        st.download_button(
                            "📥 Download (free — your note)",
                            data=f.read(),
                            file_name=f"{note['title']}.{note['file_type']}",
                            mime="application/octet-stream",
                            key=f"dl_own_{note['id']}",
                        )
                except FileNotFoundError:
                    st.error("File not found on server.")
            else:
                current_points = db.get_points_balance(st.session_state.user_id)
                if current_points < POINTS_PER_DOWNLOAD:
                    st.error(f"Not enough points. You have {current_points}, need {POINTS_PER_DOWNLOAD}.")
                else:
                    try:
                        with open(note["file_path"], "rb") as f:
                            file_data = f.read()

                        if st.download_button(
                            f"📥 Download ({POINTS_PER_DOWNLOAD} points)",
                            data=file_data,
                            file_name=f"{note['title']}.{note['file_type']}",
                            mime="application/octet-stream",
                            key=f"dl_{note['id']}",
                        ):
                            db.deduct_points(
                                st.session_state.user_id,
                                POINTS_PER_DOWNLOAD,
                                f"Downloaded: {note['title']}",
                            )
                            st.session_state.points = db.get_points_balance(st.session_state.user_id)
                    except FileNotFoundError:
                        st.error("File not found on server.")

            # ── Rating (Pair 2 will enhance this) ──
            if st.session_state.get("user_id") and note["user_id"] != st.session_state.user_id:
                st.divider()
                existing_rating = db.get_user_rating(st.session_state.user_id, note["id"])
                selected_stars = st.slider(
                    "Rate this note",
                    min_value=1,
                    max_value=5,
                    value=existing_rating or 3,
                    key=f"rate_{note['id']}",
                )
                if st.button("Submit rating", key=f"rate_btn_{note['id']}"):
                    db.add_rating(st.session_state.user_id, note["id"], selected_stars)
                    if selected_stars >= 4:
                        from config import POINTS_PER_UPVOTE
                        db.award_points(
                            note["user_id"],
                            POINTS_PER_UPVOTE,
                            f"High rating on: {note['title']}",
                        )
                    st.success("Rating submitted!")
                    st.rerun()
