"""
NovaNotes — Horizontal top navigation bar rendered on every page.
"""

import base64
import html as html_lib
from pathlib import Path

import streamlit as st


def _logo_b64() -> str:
    logo_path = Path(__file__).parent.parent / "static" / "logo.png"
    return base64.b64encode(logo_path.read_bytes()).decode()


def _nav_items(is_admin: bool):
    items = [
        ("Home", "app.py"),
        ("Browse Notes", "pages/2_Browse.py"),
        ("Upload", "pages/3_Upload.py"),
        ("Reviews", "pages/4_Reviews.py"),
        ("My Account", "pages/5_Profile.py"),
    ]
    if is_admin:
        items.append(("Admin", "pages/6_Admin.py"))
    return items


def render_top_nav(current_page: str = "Home"):
    """Render the horizontal top nav. `current_page` matches one of the labels."""
    is_logged_in = bool(st.session_state.get("user_id"))
    is_admin = bool(st.session_state.get("is_admin"))

    items = _nav_items(is_admin)

    col_specs = [2.2] + [1] * len(items) + [2.4]
    cols = st.columns(col_specs, gap="small")

    with cols[0]:
        logo = _logo_b64()
        st.markdown(
            '<div class="top-nav-marker"></div>'
            f'<div class="nav-brand"><a href="/" target="_self" style="display:inline-block;">'
            f'<img src="data:image/png;base64,{logo}" '
            f'style="height:52px;vertical-align:middle;object-fit:contain;cursor:pointer;" /></a></div>',
            unsafe_allow_html=True,
        )

    for i, (label, target) in enumerate(items):
        with cols[i + 1]:
            btype = "primary" if label == current_page else "secondary"
            if st.button(label, key=f"nav_{label}", type=btype, use_container_width=True):
                st.switch_page(target)

    with cols[-1]:
        if is_logged_in:
            pts = st.session_state.get("points", 0)
            uname = html_lib.escape(st.session_state.get("username", ""))
            sub_info, sub_btn = st.columns([1.3, 1], gap="small")
            with sub_info:
                st.markdown(
                    f'<div class="nav-user">'
                    f'<span class="nav-username">👤 {uname}</span>'
                    f'<span class="points-badge">⭐ {pts}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with sub_btn:
                btype = "primary" if current_page == "Logout" else "secondary"
                if st.button("Logout", key="nav_logout", type=btype, use_container_width=True):
                    for key in ["user_id", "username", "is_admin"]:
                        st.session_state[key] = None
                    st.session_state.is_admin = False
                    st.session_state.points = 0
                    st.rerun()
        else:
            btype = "primary" if current_page == "Login" else "secondary"
            if st.button("Login", key="nav_login", type=btype, use_container_width=True):
                st.switch_page("pages/1_Login.py")

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
