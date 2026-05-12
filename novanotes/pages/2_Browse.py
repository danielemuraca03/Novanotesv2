"""
NovaNotes — Page 2: Browse Notes
"""

import html as html_lib
import streamlit as st
import db
from config import POINTS_PER_DOWNLOAD, POINTS_PER_UPVOTE
from utils.style import get_custom_css
from utils.navbar import render_top_nav

st.set_page_config(page_title="NovaNotes — Browse", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
st.markdown(get_custom_css(), unsafe_allow_html=True)
render_top_nav("Browse Notes")

st.markdown("# 📖 Browse notes")

# ── Pre-populate search from home page ───────────
_initial_search = st.session_state.pop("home_search", "")

# ── Filters ──────────────────────────────────────
col_search, col_course, col_prof, col_sort = st.columns([2, 1.5, 1.5, 1])

with col_search:
    search_query = st.text_input(
        "Search", placeholder="🔍  e.g. microeconomics midterm",
        label_visibility="collapsed",
        value=_initial_search,
    )

courses = ["All"] + db.get_all_courses()
professors = ["All"] + db.get_all_professors()

with col_course:
    selected_course = st.selectbox("Course", courses, label_visibility="collapsed")
with col_prof:
    selected_prof = st.selectbox("Professor", professors, label_visibility="collapsed")
with col_sort:
    sort_by = st.selectbox("Sort", ["Newest", "Top rated"], label_visibility="collapsed")

# ── Fetch ──────────────────────────────────────────
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
st.markdown("<br>", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────
def file_badge(file_type: str) -> str:
    ft = (file_type or "file").lower().strip()
    css_cls = ft if ft in ("pdf", "docx", "png", "jpg", "jpeg") else "other"
    return f'<span class="badge badge-{css_cls}">{ft.upper()}</span>'


def render_stars(avg: float, count: int) -> str:
    filled = round(avg)
    stars_html = "★" * filled + "☆" * (5 - filled)
    return (
        f'<span class="stars">{stars_html}</span>'
        f'<span style="font-size:12px;color:#9e9e9e;margin-left:5px;">({count})</span>'
    )


# ── Note cards ────────────────────────────────────
for note in notes:
    title  = html_lib.escape(note["title"])
    course = html_lib.escape(note["course"])
    prof   = html_lib.escape(note["professor"])
    uname  = html_lib.escape(note["username"])
    year_str = f" · {note['year']}" if note["year"] else ""
    date_str = str(note["created_at"])[:10]

    st.markdown(f"""
    <div class="note-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px;">
            {file_badge(note['file_type'])}
            <span style="font-size:12px;color:#9e9e9e;">by {uname} · {date_str}</span>
        </div>
        <div style="font-size:16px;font-weight:600;color:#111;margin-bottom:3px;">{title}</div>
        <div style="font-size:13px;color:#666;margin-bottom:12px;">{course} · Prof. {prof}{year_str}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>{render_stars(note['avg_rating'], note['rating_count'])}</div>
            <span class="cost-tag">⭐ {POINTS_PER_DOWNLOAD} pts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View details & download"):
        if note["description"]:
            st.text(note["description"])

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**File type:** `{note['file_type'].upper()}`")
        with col_b:
            st.markdown(f"**Download cost:** {POINTS_PER_DOWNLOAD} pts")

        # ── Download logic ──
        if not st.session_state.get("user_id"):
            st.warning("Log in to download this note.")
        elif note["user_id"] == st.session_state.user_id:
            try:
                with open(note["file_path"], "rb") as f:
                    st.download_button(
                        "📥 Download (free — your note)",
                        data=f.read(),
                        file_name=f"{note['title']}.{note['file_type']}",
                        mime="application/octet-stream",
                        key=f"dl_own_{note['id']}",
                        use_container_width=True,
                    )
            except FileNotFoundError:
                st.error("File not found on server.")
        else:
            current_points = db.get_points_balance(st.session_state.user_id)
            if current_points < POINTS_PER_DOWNLOAD:
                st.error(
                    f"Not enough points. You have {current_points}, need {POINTS_PER_DOWNLOAD}."
                )
            else:
                try:
                    with open(note["file_path"], "rb") as f:
                        file_data = f.read()

                    if st.download_button(
                        f"📥 Download ({POINTS_PER_DOWNLOAD} pts)",
                        data=file_data,
                        file_name=f"{note['title']}.{note['file_type']}",
                        mime="application/octet-stream",
                        key=f"dl_{note['id']}",
                        use_container_width=True,
                    ):
                        db.deduct_points(
                            st.session_state.user_id,
                            POINTS_PER_DOWNLOAD,
                            f"Downloaded: {note['title']}",
                        )
                        st.session_state.points = db.get_points_balance(
                            st.session_state.user_id
                        )
                except FileNotFoundError:
                    st.error("File not found on server.")

        # ── Rating ──
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
                if selected_stars >= 4 and existing_rating is None:
                    db.award_points(
                        note["user_id"],
                        POINTS_PER_UPVOTE,
                        f"High rating on: {note['title']}",
                    )
                st.success("Rating submitted!")
                st.rerun()
