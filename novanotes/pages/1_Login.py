"""
NovaNotes — Page 1: Login & Register
"""

import streamlit as st
import bcrypt
import db
from config import ALLOWED_EMAIL_DOMAIN, INITIAL_POINTS, ADMIN_EMAILS
from utils.style import get_custom_css
from utils.navbar import render_top_nav

st.set_page_config(page_title="NovaNotes — Login", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
st.markdown(get_custom_css(), unsafe_allow_html=True)
render_top_nav("Login")

# ── If already logged in, redirect ──
if st.session_state.get("user_id"):
    st.success(f"You're already logged in as **{st.session_state.username}**.")
    st.info("Use the top navigation to move around.")
    st.stop()

st.markdown("# 🔐 Login or Register")
st.caption(f"Access is restricted to **@{ALLOWED_EMAIL_DOMAIN}** addresses.")
st.markdown("<br>", unsafe_allow_html=True)

tab_login, tab_register = st.tabs(["Login", "Create account"])

# ══════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════
with tab_login:
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.name@novasbe.pt")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in", use_container_width=True)

    if submitted:
        if not email or not password:
            st.error("Please fill in both fields.")
        else:
            user = db.get_user_by_email(email.strip().lower())
            if user is None:
                st.error("No account found with this email.")
            elif user["is_banned"]:
                st.error("This account has been suspended.")
            elif not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
                st.error("Incorrect password.")
            else:
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.session_state.is_admin = bool(user["is_admin"])
                st.session_state.points = user["points"]
                st.success("Logged in successfully!")
                st.rerun()

# ══════════════════════════════════════════════
#  REGISTER
# ══════════════════════════════════════════════
with tab_register:
    with st.form("register_form"):
        reg_username = st.text_input("Display name", placeholder="E.g. Maria S.")
        reg_email = st.text_input("Nova SBE email", placeholder="E.g. 12345@novasbe.pt")
        reg_password = st.text_input("Password", type="password", key="reg_pw")
        reg_confirm = st.text_input("Confirm password", type="password", key="reg_cf")
        submitted_reg = st.form_submit_button("Create account", use_container_width=True)

    if submitted_reg:
        errors = []

        if not reg_username or not reg_email or not reg_password:
            errors.append("All fields are required.")

        email_clean = reg_email.strip().lower()
        if not email_clean.endswith(f"@{ALLOWED_EMAIL_DOMAIN}"):
            errors.append(f"Email must end with @{ALLOWED_EMAIL_DOMAIN}")

        if reg_password != reg_confirm:
            errors.append("Passwords don't match.")

        if len(reg_password) < 6:
            errors.append("Password must be at least 6 characters.")

        if db.get_user_by_email(email_clean):
            errors.append("An account with this email already exists.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            pw_hash = bcrypt.hashpw(reg_password.encode(), bcrypt.gensalt()).decode()
            is_admin = email_clean in ADMIN_EMAILS

            user_id = db.create_user(
                email=email_clean,
                username=reg_username.strip(),
                password_hash=pw_hash,
                initial_points=0,
                is_admin=is_admin,
            )

            db.verify_user(user_id)
            db.award_points(user_id, INITIAL_POINTS, "Signup bonus")

            st.success(f"Account created! You received **{INITIAL_POINTS} pts** as a welcome bonus. Log in now.")
