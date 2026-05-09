"""
NovaNotes — Email verification utility.
Sends a verification link to the user's Nova SBE email.
"""

import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st
from config import VERIFICATION_TOKEN_EXPIRY_HOURS
import db


def generate_token():
    """Generate a secure random token."""
    return secrets.token_urlsafe(32)


def send_verification_email(to_email, token):
    """
    Send a verification email with a clickable link.

    Requires these keys in .streamlit/secrets.toml:
        SMTP_EMAIL = "your-email@gmail.com"
        SMTP_PASSWORD = "your-gmail-app-password"
        APP_URL = "https://your-app.streamlit.app"
    """
    try:
        sender_email = st.secrets["SMTP_EMAIL"]
        sender_password = st.secrets["SMTP_PASSWORD"]
        app_url = st.secrets.get("APP_URL", "http://localhost:8501")

        verification_link = f"{app_url}/?token={token}"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Verify your NovaNotes account"
        msg["From"] = sender_email
        msg["To"] = to_email

        # Plain text version
        text = f"""
Welcome to NovaNotes!

Please verify your email by clicking this link:
{verification_link}

This link expires in {VERIFICATION_TOKEN_EXPIRY_HOURS} hours.

If you didn't create an account, you can ignore this email.
        """

        # HTML version (looks nicer in email clients)
        html = f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
            <h2 style="color: #1a1a2e;">Welcome to NovaNotes 📚</h2>
            <p>Please verify your email address to activate your account.</p>
            <a href="{verification_link}"
               style="display: inline-block; background: #1a1a2e; color: white;
                      padding: 12px 28px; border-radius: 8px; text-decoration: none;
                      font-weight: 500; margin: 16px 0;">
                Verify my email
            </a>
            <p style="color: #666; font-size: 13px;">
                This link expires in {VERIFICATION_TOKEN_EXPIRY_HOURS} hours.<br>
                If you didn't create an account, ignore this email.
            </p>
        </div>
        """

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())

        return True

    except Exception:
        return False


def handle_verification():
    """
    Check if the current URL contains a verification token.
    Call this at the top of app.py to auto-verify on page load.
    """
    params = st.query_params
    if "token" in params:
        token_str = params["token"]
        token_row = db.get_verification_token(token_str)

        if token_row:
            user_id = token_row["user_id"]
            db.verify_user(user_id)
            db.mark_token_used(token_str)
            st.success("✅ Email verified! You can now log in.")
            # Clean the URL
            st.query_params.clear()
        else:
            st.error("Invalid or expired verification link.")
            st.query_params.clear()
