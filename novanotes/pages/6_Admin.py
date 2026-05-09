"""
NovaNotes — Page 6: Admin Panel
(Pair 2 builds this page)
"""

import streamlit as st
import db
from utils.style import get_custom_css

st.set_page_config(page_title="NovaNotes — Admin", page_icon="📚", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── Admin guard ──
if not st.session_state.get("user_id") or not st.session_state.get("is_admin"):
    st.error("Access denied. Admin accounts only.")
    st.stop()

st.markdown("# 🛡️ Admin panel")

# ── Platform stats ──
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

tab_flags, tab_users = st.tabs(["Flagged content", "User management"])

# ══════════════════════════════════════════════
#  FLAGGED CONTENT
# ══════════════════════════════════════════════
with tab_flags:
    flags = db.get_pending_flags()

    if not flags:
        st.success("No pending flags. All clear!")
    else:
        for flag in flags:
            with st.container():
                st.markdown(
                    f"""<div class="note-card" style="border-left: 3px solid #e63946;">
                        <p style="margin:0; font-size:13px; color:#e63946; font-weight:500;">
                            🚩 {flag["content_type"].upper()} #{flag["content_id"]}
                        </p>
                        <p style="margin:4px 0; font-size:14px;">{flag["reason"]}</p>
                        <p style="margin:0; color:#999; font-size:12px;">
                            Reported by {flag["reporter_name"]} · {str(flag["created_at"])[:10]}
                        </p>
                    </div>""",
                    unsafe_allow_html=True,
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Dismiss", key=f"dismiss_{flag['id']}"):
                        db.resolve_flag(flag["id"])
                        st.rerun()
                with col2:
                    if st.button("🗑️ Remove content", key=f"remove_{flag['id']}"):
                        if flag["content_type"] == "note":
                            db.remove_note(flag["content_id"])
                        elif flag["content_type"] == "review":
                            db.remove_review(flag["content_id"])
                        db.resolve_flag(flag["id"])
                        st.success("Content removed.")
                        st.rerun()
                with col3:
                    pass  # spacer
                st.divider()

# ══════════════════════════════════════════════
#  USER MANAGEMENT
# ══════════════════════════════════════════════
with tab_users:
    users = db.get_all_users()

    for user in users:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            status = ""
            if user["is_banned"]:
                status = "🚫 Banned"
            elif not user["is_verified"]:
                status = "⏳ Unverified"
            elif user["is_admin"]:
                status = "👑 Admin"
            else:
                status = "✅ Active"

            st.markdown(f"**{user['username']}** ({user['email']})")
            st.caption(f"{status} · ⭐ {user['points']} points · Joined {str(user['created_at'])[:10]}")

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

        with col3:
            pass  # spacer
        st.divider()
