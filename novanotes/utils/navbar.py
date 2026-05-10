"""
NovaNotes — Top navigation bar rendered on every page.
"""

import html as html_lib
import streamlit as st


def render_navbar():
    """Render the top navbar: logo left, login/user right."""
    # Marker div — CSS :has(.nav-marker) targets the sibling columns row to make it fixed/full-width
    st.markdown('<div class="nav-marker"></div>', unsafe_allow_html=True)

    col_logo, col_mid, col_right = st.columns([1.8, 6, 1.8])

    with col_logo:
        st.page_link("app.py", label="📚 **NovaNotes**")

    with col_right:
        if st.session_state.get("user_id"):
            pts   = st.session_state.get("points", 0)
            uname = html_lib.escape(st.session_state.get("username", ""))
            st.markdown(
                f'<div style="text-align:right;padding-top:6px;">'
                f'<span style="font-size:14px;color:#444;">👤 <strong>{uname}</strong></span>'
                f'&nbsp;&nbsp;'
                f'<span class="points-badge" style="font-size:13px;padding:4px 12px;">⭐ {pts}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="nav-login-wrap">', unsafe_allow_html=True)
            st.page_link("pages/1_Login.py", label="Log in →")
            st.markdown("</div>", unsafe_allow_html=True)

    # No HR here — the fixed navbar bar already has a border-bottom in CSS
