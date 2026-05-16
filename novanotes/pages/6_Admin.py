"""
NovaNotes — Page 6: Admin Panel
"""

import html as html_lib
import os
import streamlit as st
import db
from config import POINTS_PER_UPLOAD
from utils.style import get_custom_css
from utils.navbar import render_top_nav


def _badge_for_file_type(ft):
    cls = f"badge badge-{ft.lower()}" if ft.lower() in ("pdf", "docx", "png", "jpg", "jpeg") else "badge badge-other"
    return f'<span class="{cls}">{html_lib.escape(ft.upper())}</span>'


def _render_note_card(note, key_prefix):
    """Render one note row with Flag/Unflag + Delete buttons. Matches admin card style."""
    title_esc    = html_lib.escape(note["title"])
    course_esc   = html_lib.escape(note["course"])
    uploader_esc = html_lib.escape(note["username"])
    date_str     = str(note["created_at"])[:10]
    is_flagged   = bool(note["flagged"])

    border_color = "#e53935" if is_flagged else "#ebebeb"
    flag_label_html = (
        '<span style="color:#e53935;font-weight:700;font-size:11px;letter-spacing:0.5px;'
        'text-transform:uppercase;margin-right:8px;">⚠️ Flagged</span>'
        if is_flagged else ""
    )

    st.markdown(f"""
    <div class="note-card" style="border-left: 3px solid {border_color};">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;">
            <div style="flex:1;min-width:0;">
                <div style="font-size:15px;font-weight:600;color:#111;margin-bottom:3px;">
                    {flag_label_html}{title_esc}
                </div>
                <div style="font-size:13px;color:#777;margin-bottom:3px;">
                    {course_esc} · uploaded by <strong>{uploader_esc}</strong>
                </div>
                <div style="font-size:12px;color:#aaa;display:flex;align-items:center;gap:8px;">
                    <span>{date_str}</span>
                    <span>·</span>
                    {_badge_for_file_type(note["file_type"])}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_flag, col_delete, _ = st.columns([1, 1, 3])
    with col_flag:
        if is_flagged:
            if st.button("✅ Unflag", key=f"{key_prefix}_unflag_{note['id']}", use_container_width=True):
                db.set_note_flagged(note["id"], False)
                st.rerun()
        else:
            if st.button("🚩 Flag", key=f"{key_prefix}_flag_{note['id']}", use_container_width=True):
                db.set_note_flagged(note["id"], True)
                st.rerun()
    with col_delete:
        if st.button("🗑️ Delete", key=f"{key_prefix}_delete_{note['id']}", use_container_width=True):
            removed = db.hard_delete_note(note["id"])
            if removed is not None:
                if removed["file_path"]:
                    try:
                        os.remove(removed["file_path"])
                    except (FileNotFoundError, OSError):
                        pass
                db.revert_upload_points(
                    removed["user_id"],
                    POINTS_PER_UPLOAD,
                    f"Admin removed upload: {removed['title']}",
                )
                st.success(f"Deleted '{removed['title']}' and reverted {POINTS_PER_UPLOAD} pts from uploader.")
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

st.set_page_config(page_title="NovaNotes — Admin", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
st.markdown(get_custom_css(), unsafe_allow_html=True)
render_top_nav("Admin")

# ── Admin guard ──
if not st.session_state.get("user_id") or not st.session_state.get("is_admin"):
    st.error("Access denied. Admin accounts only.")
    st.stop()

st.markdown("# 🛡️ Admin panel")

# ── Platform stats ──────────────────────────────
stats = db.get_stats()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Users", stats["total_users"])
with col2:
    st.metric("Notes", stats["total_notes"])
with col3:
    st.metric("Reviews", stats["total_reviews"])
with col4:
    st.metric("Downloads", stats["total_downloads"])
with col5:
    st.metric("Pending flags", stats["pending_flags"])

st.divider()

tab_flags, tab_notes, tab_users = st.tabs(["Flagged content", "Manage notes", "User management"])

# ══════════════════════════════════════════════
#  FLAGGED CONTENT
# ══════════════════════════════════════════════
with tab_flags:
    flags = db.get_pending_flags()

    if not flags:
        st.success("No pending flags — all clear!")
    else:
        for flag in flags:
            reason_esc   = html_lib.escape(flag["reason"])
            reporter_esc = html_lib.escape(flag["reporter_name"])
            date_str     = str(flag["created_at"])[:10]
            content_type = flag["content_type"].upper()

            st.markdown(f"""
            <div class="review-card" style="border-left: 3px solid #e53935;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-size:11px;font-weight:700;color:#e53935;letter-spacing:0.5px;text-transform:uppercase;">
                        🚩 {content_type} #{flag['content_id']}
                    </span>
                    <span style="font-size:12px;color:#bbb;">{date_str}</span>
                </div>
                <p style="margin:0 0 6px;font-size:14px;color:#333;">{reason_esc}</p>
                <p style="margin:0;font-size:12px;color:#aaa;">Reported by {reporter_esc}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("✅ Dismiss", key=f"dismiss_{flag['id']}"):
                    db.resolve_flag(flag["id"])
                    st.rerun()
            with col2:
                if st.button("🗑️ Remove", key=f"remove_{flag['id']}"):
                    if flag["content_type"] == "note":
                        db.remove_note(flag["content_id"])
                    elif flag["content_type"] == "review":
                        db.remove_review(flag["content_id"])
                    db.resolve_flag(flag["id"])
                    st.success("Content removed.")
                    st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  MANAGE NOTES
# ══════════════════════════════════════════════
with tab_notes:
    flagged_notes = db.get_flagged_notes()
    all_notes     = db.get_all_notes_admin()

    st.markdown("### ⚠️ Flagged notes")
    if not flagged_notes:
        st.success("No flagged notes.")
    else:
        for note in flagged_notes:
            _render_note_card(note, key_prefix="flagged")

    st.divider()

    st.markdown(f"### 📚 All notes ({len(all_notes)})")
    if not all_notes:
        st.info("No notes have been uploaded yet.")
    else:
        for note in all_notes:
            _render_note_card(note, key_prefix="all")

# ══════════════════════════════════════════════
#  USER MANAGEMENT
# ══════════════════════════════════════════════
with tab_users:
    users = db.get_all_users()

    for user in users:
        username_esc = html_lib.escape(user["username"])
        email_esc    = html_lib.escape(user["email"])

        if user["is_banned"]:
            status_html = '<span style="color:#e53935;font-weight:600;font-size:12px;">🚫 Banned</span>'
        elif user["is_admin"]:
            status_html = '<span style="color:#7b1fa2;font-weight:600;font-size:12px;">👑 Admin</span>'
        else:
            status_html = '<span style="color:#00ab6b;font-weight:600;font-size:12px;">✅ Active</span>'

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style="padding:8px 0;">
                <div style="font-size:14px;font-weight:600;color:#111;">{username_esc}</div>
                <div style="font-size:12px;color:#888;">{email_esc}</div>
                <div style="margin-top:3px;display:flex;align-items:center;gap:10px;">
                    {status_html}
                    <span style="font-size:12px;color:#aaa;">⭐ {user['points']} pts · joined {str(user['created_at'])[:10]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if not user["is_admin"]:
                if user["is_banned"]:
                    if st.button("Unban", key=f"unban_{user['id']}"):
                        db.unban_user(user["id"])
                        st.rerun()
                else:
                    if st.button("Ban", key=f"ban_{user['id']}"):
                        db.ban_user(user["id"])
                        st.rerun()
        st.divider()
