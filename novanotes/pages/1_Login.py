"""
NovaNotes — Page 1: Login & Register
"""

import streamlit as st
import bcrypt
import db
from config import ALLOWED_EMAIL_DOMAIN, INITIAL_POINTS, ADMIN_EMAILS
from utils.style import get_custom_css
from utils.email_verify import generate_token, send_verification_email, handle_verification

st.set_page_config(page_title="NovaNotes — Login", page_icon="📚", layout="centered")
st.markdown(get_custom_css(), unsafe_allow_html=True)
handle_verification()

# ── If already logged in, redirect ──
if st.session_state.get("user_id"):
    st.success(f"You're already logged in as **{st.session_state.username}**.")
    st.info("Use the sidebar to navigate.")
    st.stop()

st.markdown("# 🔐 Login or Register")

tab_login, tab_register = st.tabs(["Login", "Register"])

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
            elif not user["is_verified"]:
                st.warning("Please verify your email first. Check your inbox.")
            else:
                # Successful login
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.session_state.is_admin = bool(user["is_admin"])
                st.session_state.points = user["points"]
                st.success("Logged in!")
                st.rerun()

# ══════════════════════════════════════════════
#  REGISTER
# ══════════════════════════════════════════════
with tab_register:
    with st.form("register_form"):
        reg_username = st.text_input("Display name", placeholder="Maria S.")
        reg_email = st.text_input("Nova SBE email", placeholder="12345@novasbe.pt")
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
            # Hash password
            pw_hash = bcrypt.hashpw(reg_password.encode(), bcrypt.gensalt()).decode()

            # Check if admin
            is_admin = email_clean in ADMIN_EMAILS

            # Create user
            user_id = db.create_user(
                email=email_clean,
                username=reg_username.strip(),
                password_hash=pw_hash,
                initial_points=INITIAL_POINTS,
                is_admin=is_admin,
            )

            # Log the signup bonus
            db.award_points(user_id, INITIAL_POINTS, "Signup bonus")

            # Generate and send verification token
            token = generate_token()
            db.create_verification_token(user_id, token)

            email_sent = send_verification_email(email_clean, token)

            if email_sent:
                st.success(
                    "Account created! Check your email for a verification link. "
                    "You must verify before logging in."
                )
            else:
                db.verify_user(user_id)
                st.success(
                    "Account created! You can now log in."
                )
