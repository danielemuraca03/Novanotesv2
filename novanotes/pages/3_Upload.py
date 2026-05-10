"""
NovaNotes — Page 3: Upload Notes
"""

import os
import uuid
import html as html_lib
import streamlit as st
import db
from config import (
    ALLOWED_FILE_TYPES,
    MAX_FILE_SIZE_MB,
    UPLOAD_FOLDER,
    POINTS_PER_UPLOAD,
)
from utils.style import get_custom_css
from utils.navbar import render_navbar

st.set_page_config(page_title="NovaNotes — Upload", page_icon="📚", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)
render_navbar()

# ── Login guard ──
if not st.session_state.get("user_id"):
    st.warning("Please log in to upload notes.")
    st.stop()

# ── Page header ──
st.markdown("# 📤 Upload notes")

st.markdown(f"""
<div class="upload-banner">
    <div class="ub-icon">🎁</div>
    <div>
        <p class="ub-title">Earn {POINTS_PER_UPLOAD} points per upload</p>
        <p class="ub-sub">
            Share your class notes and help fellow students —
            accepted formats: {', '.join(f.upper() for f in ALLOWED_FILE_TYPES)} · max {MAX_FILE_SIZE_MB} MB
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Ensure upload folder exists ──
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Upload form ──
with st.form("upload_form"):
    title = st.text_input("Title *", placeholder="e.g. Microeconomics Midterm Summary")

    col1, col2 = st.columns(2)
    with col1:
        course = st.text_input("Course *", placeholder="e.g. Microeconomics I")
    with col2:
        professor = st.text_input("Professor *", placeholder="e.g. Prof. Santos")

    col3, col4 = st.columns(2)
    with col3:
        year = st.number_input("Year", min_value=2015, max_value=2030, value=2025)
    with col4:
        st.markdown("&nbsp;")

    description = st.text_area(
        "Description (optional)",
        placeholder="Brief summary of what's covered in these notes...",
        max_chars=500,
    )

    uploaded_file = st.file_uploader(
        "Upload your file *",
        type=ALLOWED_FILE_TYPES,
        help=f"Accepted: {', '.join(ALLOWED_FILE_TYPES).upper()} — Max {MAX_FILE_SIZE_MB} MB",
    )

    submitted = st.form_submit_button("📤 Upload & earn points", use_container_width=True)

if submitted:
    errors = []

    if not title or not title.strip():
        errors.append("Title is required.")
    if not course or not course.strip():
        errors.append("Course is required.")
    if not professor or not professor.strip():
        errors.append("Professor is required.")
    if uploaded_file is None:
        errors.append("Please select a file to upload.")
    elif uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        errors.append(f"File is too large. Maximum is {MAX_FILE_SIZE_MB} MB.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        original_name = uploaded_file.name
        file_ext = original_name.rsplit(".", 1)[-1].lower()
        unique_name = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        note_id = db.save_note(
            user_id=st.session_state.user_id,
            title=title.strip(),
            course=course.strip(),
            professor=professor.strip(),
            year=year,
            description=description.strip() if description else "",
            file_path=file_path,
            file_type=file_ext,
        )

        db.award_points(
            st.session_state.user_id,
            POINTS_PER_UPLOAD,
            f"Uploaded: {title.strip()}",
        )
        st.session_state.points = db.get_points_balance(st.session_state.user_id)

        st.success(f"Note uploaded successfully! You earned **{POINTS_PER_UPLOAD} points** ⭐")
        st.balloons()

# ── My uploads ────────────────────────────────────
st.divider()
st.markdown("### Your uploads")

my_notes = db.get_notes_by_user(st.session_state.user_id)

if not my_notes:
    st.info("You haven't uploaded any notes yet. Use the form above to get started!")
else:
    for note in my_notes:
        title_esc = html_lib.escape(note["title"])
        course_esc = html_lib.escape(note["course"])
        prof_esc = html_lib.escape(note["professor"])
        avg = round(note["avg_rating"], 1)
        stars_filled = round(note["avg_rating"])
        stars_html = "★" * stars_filled + "☆" * (5 - stars_filled)
        date_str = str(note["created_at"])[:10]

        st.markdown(f"""
        <div class="note-card" style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:15px;font-weight:600;color:#111;margin-bottom:2px;">{title_esc}</div>
                <div style="font-size:13px;color:#777;">{course_esc} · Prof. {prof_esc} · {date_str}</div>
            </div>
            <div style="text-align:right;flex-shrink:0;margin-left:16px;">
                <span class="stars-sm">{stars_html}</span>
                <div style="font-size:12px;color:#9e9e9e;margin-top:2px;">{avg} ({note['rating_count']} ratings)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
