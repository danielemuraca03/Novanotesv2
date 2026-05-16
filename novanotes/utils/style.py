"""
NovaNotes — Custom CSS styling (Studocu-inspired redesign).
"""


def get_custom_css():
    return """
    <style>
    /* ─── Font ─── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* ─── Layout ─── */
    .main .block-container,
    [data-testid="stMain"] .block-container,
    [data-testid="stAppViewContainer"] .block-container {
        padding-top: 0 !important;
        padding-bottom: 4rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1400px !important;
    }

    /* ─── Remove Streamlit chrome ─── */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }

    /* ─── Hide sidebar entirely ─── */
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
    }

    /* ══════════════════════════════════════════
       TYPOGRAPHY
    ══════════════════════════════════════════ */
    h1 {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #0d0d0d !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 6px !important;
        line-height: 1.2 !important;
    }
    h2 {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #111 !important;
        margin-bottom: 6px !important;
    }
    h3 {
        font-size: 19px !important;
        font-weight: 600 !important;
        color: #111 !important;
    }
    p, .stMarkdown p {
        font-size: 15px !important;
        line-height: 1.65 !important;
    }

    /* ══════════════════════════════════════════
       BUTTONS
    ══════════════════════════════════════════ */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border: 1px solid #e0e0e0 !important;
        color: #444 !important;
        background: white !important;
        transition: border-color 0.15s, color 0.15s !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        border-color: #00ab6b !important;
        color: #00ab6b !important;
        transform: none !important;
        box-shadow: none !important;
        background: white !important;
    }
    /* Primary / form submit */
    [data-testid="stFormSubmitButton"] > button {
        background: #00ab6b !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        padding: 0.45rem 1.5rem !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background: #009960 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    /* Download buttons */
    [data-testid="stDownloadButton"] > button {
        background: #00ab6b !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border-radius: 6px !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: #009960 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* ══════════════════════════════════════════
       FORM INPUTS
    ══════════════════════════════════════════ */
    [data-testid="stTextInput"] > div > input,
    [data-testid="stTextArea"] > div > textarea,
    [data-testid="stNumberInput"] input {
        border-radius: 6px !important;
        border-color: #ddd !important;
        font-size: 14px !important;
        color: #1a1a1a !important;
        background: white !important;
    }
    [data-testid="stTextInput"] > div > input:focus,
    [data-testid="stTextArea"] > div > textarea:focus {
        border-color: #00ab6b !important;
        box-shadow: 0 0 0 2px rgba(0,171,107,0.14) !important;
    }
    /* Selectbox */
    [data-baseweb="select"] > div:first-child {
        border-radius: 6px !important;
        border-color: #ddd !important;
        font-size: 14px !important;
        background: white !important;
    }
    [data-baseweb="select"] > div:first-child:focus-within {
        border-color: #00ab6b !important;
        box-shadow: 0 0 0 2px rgba(0,171,107,0.14) !important;
    }
    /* Slider */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: #00ab6b !important;
        border-color: #00ab6b !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stTickBarMin"]~div:first-of-type {
        background: #00ab6b !important;
    }

    /* ══════════════════════════════════════════
       TABS
    ══════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 0 !important;
        border-bottom: 2px solid #ebebeb;
        padding-bottom: 0 !important;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        color: #666 !important;
        padding: 10px 22px !important;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #00ab6b !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"][data-baseweb="tab"] {
        color: #00ab6b !important;
        border-bottom-color: #00ab6b !important;
        background: transparent !important;
        font-weight: 600 !important;
    }

    /* ══════════════════════════════════════════
       METRICS
    ══════════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: white !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        border: 1px solid #ebebeb !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
    [data-testid="stMetric"] label {
        color: #999 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #111 !important;
    }

    /* ══════════════════════════════════════════
       ALERTS
    ══════════════════════════════════════════ */
    .stAlert {
        border-radius: 8px !important;
        font-size: 14px !important;
    }

    /* ══════════════════════════════════════════
       FILE UPLOADER
    ══════════════════════════════════════════ */
    [data-testid="stFileUploaderDropzone"] {
        border-radius: 8px !important;
        border: 2px dashed #d0d0d0 !important;
        background: #fafafa !important;
        padding: 24px !important;
        transition: border-color 0.15s !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #00ab6b !important;
    }

    /* ══════════════════════════════════════════
       DIVIDER
    ══════════════════════════════════════════ */
    hr {
        border: none !important;
        border-top: 1px solid #ebebeb !important;
        margin: 1rem 0 !important;
    }

    /* ══════════════════════════════════════════
       NOTE & REVIEW CARDS
    ══════════════════════════════════════════ */
    .note-card, .review-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 10px;
        transition: box-shadow 0.15s, border-color 0.15s;
    }
    .note-card:hover, .review-card:hover {
        box-shadow: 0 6px 22px rgba(0,0,0,0.08);
        border-color: #c8c8c8;
    }

    /* ══════════════════════════════════════════
       FILE TYPE BADGES
    ══════════════════════════════════════════ */
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        vertical-align: middle;
    }
    .badge-pdf   { background: #fde8e8; color: #c62828; }
    .badge-docx  { background: #e3f2fd; color: #1565c0; }
    .badge-png,
    .badge-jpg,
    .badge-jpeg  { background: #e8f5e9; color: #2e7d32; }
    .badge-other { background: #f3e5f5; color: #6a1b9a; }

    /* ══════════════════════════════════════════
       POINTS & COST BADGES
    ══════════════════════════════════════════ */
    .points-badge {
        display: inline-block;
        background: #e6f7f1;
        color: #00ab6b;
        border: 1px solid #b2dfcf;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }
    .cost-tag {
        display: inline-block;
        background: #fff8e1;
        color: #e65100;
        border: 1px solid #ffe082;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    /* ══════════════════════════════════════════
       STARS
    ══════════════════════════════════════════ */
    .stars    { color: #ffc107; font-size: 15px; letter-spacing: 1px; }
    .stars-sm { color: #ffc107; font-size: 13px; letter-spacing: 0.5px; }
    .stars-dim { color: #e0e0e0; }

    /* ══════════════════════════════════════════
       HERO BANNER (landing page)
    ══════════════════════════════════════════ */
    .hero-banner {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 14px;
        padding: 56px 52px;
        margin-bottom: 36px;
    }
    .hero-banner h1 {
        color: white !important;
        font-size: 42px !important;
        margin-bottom: 14px !important;
        letter-spacing: -0.8px !important;
    }
    .hero-banner p {
        color: #8888b0;
        font-size: 18px !important;
        margin: 0;
        line-height: 1.65;
    }
    .hero-accent { color: #00ab6b; }

    /* ══════════════════════════════════════════
       FEATURE CARDS (landing page)
    ══════════════════════════════════════════ */
    .feature-card {
        background: white;
        border: 1px solid #ebebeb;
        border-radius: 12px;
        padding: 28px 20px;
        text-align: center;
        height: 100%;
        transition: box-shadow 0.15s;
    }
    .feature-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
    .fc-icon  { font-size: 34px; margin-bottom: 12px; }
    .fc-title { font-weight: 700; color: #111; font-size: 16px; margin-bottom: 6px; }
    .fc-desc  { color: #777; font-size: 14px; line-height: 1.55; }

    /* ══════════════════════════════════════════
       UPLOAD BANNER
    ══════════════════════════════════════════ */
    .upload-banner {
        background: linear-gradient(135deg, #00ab6b 0%, #007a4c 100%);
        border-radius: 10px;
        padding: 18px 24px;
        color: white;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .ub-icon  { font-size: 30px; line-height: 1; flex-shrink: 0; }
    .ub-title { font-size: 16px; font-weight: 600; margin: 0 0 3px; color: white; }
    .ub-sub   { font-size: 13px; opacity: 0.85; margin: 0; color: white; }

    /* ══════════════════════════════════════════
       PROFILE HEADER
    ══════════════════════════════════════════ */
    .profile-header {
        background: white;
        border: 1px solid #ebebeb;
        border-radius: 10px;
        padding: 22px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .avatar-circle {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00ab6b, #007a4c);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 22px;
        font-weight: 700;
        flex-shrink: 0;
    }

    /* ══════════════════════════════════════════
       LEADERBOARD ROWS
    ══════════════════════════════════════════ */
    .lb-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
        background: #fafafa;
        border: 1px solid #f0f0f0;
        transition: background 0.12s;
    }
    .lb-row:hover { background: #f0faf5; }
    .lb-row.lb-me { background: #e6f7f1 !important; border-color: #b2dfcf !important; }

    /* ══════════════════════════════════════════
       UPLOAD LIST (my uploads section)
    ══════════════════════════════════════════ */
    .upload-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #f2f2f2;
    }
    .upload-row:last-child { border-bottom: none; }

    /* ══════════════════════════════════════════
       POINTS HISTORY
    ══════════════════════════════════════════ */
    .pts-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #f4f4f4;
    }
    .pts-row:last-child { border-bottom: none; }

    /* ══════════════════════════════════════════
       TOP NAVIGATION BAR
       Identified by the .top-nav-marker placed in the first column
       of the navbar's st.columns() row.
    ══════════════════════════════════════════ */
    .top-nav-marker { display: none; }

    /* Brand text on the left of the nav */
    .nav-brand {
        font-size: 22px;
        font-weight: 800;
        color: #111;
        letter-spacing: -0.4px;
        line-height: 40px;
        white-space: nowrap;
    }

    /* User info block (username + points pill) on the right */
    .nav-user {
        display: flex;
        align-items: center;
        gap: 8px;
        justify-content: flex-end;
        flex-wrap: wrap;
        line-height: 40px;
    }
    .nav-username {
        font-size: 13px;
        color: #444;
        font-weight: 500;
        white-space: nowrap;
    }
    .nav-user .points-badge {
        padding: 3px 11px;
        font-size: 13px;
    }

    /* The navbar row itself: fixed at top, full width, sticky header */
    [data-testid="stHorizontalBlock"]:has(.top-nav-marker) {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        z-index: 9999 !important;
        background: white !important;
        padding: 10px 2.5rem !important;
        margin: 0 !important;
        border-bottom: 1px solid #e8e8e8 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
        align-items: center !important;
        box-sizing: border-box !important;
    }

    /* All buttons inside the nav row */
    [data-testid="stHorizontalBlock"]:has(.top-nav-marker) .stButton > button {
        background: white !important;
        color: #1a1a2e !important;
        border: 1px solid transparent !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 8px 10px !important;
        box-shadow: none !important;
        transition: color 0.12s, background 0.12s, border-color 0.12s !important;
    }
    [data-testid="stHorizontalBlock"]:has(.top-nav-marker) .stButton > button:hover {
        background: #f5f9f7 !important;
        color: #00ab6b !important;
        border-color: transparent !important;
        border-bottom-color: rgba(0,171,107,0.35) !important;
        transform: none !important;
        box-shadow: none !important;
    }
    /* Active page (rendered as type="primary") */
    [data-testid="stHorizontalBlock"]:has(.top-nav-marker) .stButton > button[kind="primary"] {
        background: white !important;
        color: #00ab6b !important;
        border-color: transparent !important;
        border-bottom-color: #00ab6b !important;
        font-weight: 700 !important;
    }
    [data-testid="stHorizontalBlock"]:has(.top-nav-marker) .stButton > button[kind="primary"]:hover {
        background: #f0faf5 !important;
        color: #00ab6b !important;
    }

    /* Spacer below the fixed navbar so content isn't hidden behind it */
    .nav-divider {
        height: 86px;
        background: transparent;
        margin: 0 0 1rem 0;
    }

    /* ══════════════════════════════════════════
       CLICKABLE LOGO
       The logo column contains the .nav-brand markup and an invisible
       st.button that triggers st.switch_page("app.py") so session state
       is preserved (a raw <a href="/"> would cause a full page reload).
       Selectors target the .st-key-nav_logo_home class Streamlit adds to
       the keyed widget's container — robust against :has() support gaps.
    ══════════════════════════════════════════ */
    [data-testid="column"]:has(.nav-brand),
    [data-testid="stColumn"]:has(.nav-brand) {
        position: relative;
    }
    [data-testid="column"]:has(.nav-brand) [data-testid="stMarkdown"],
    [data-testid="stColumn"]:has(.nav-brand) [data-testid="stMarkdown"] {
        pointer-events: none;
    }
    [data-testid="column"]:has(.nav-brand) .nav-brand,
    [data-testid="stColumn"]:has(.nav-brand) .nav-brand {
        cursor: pointer;
        pointer-events: none;
    }
    [data-testid="column"]:has(.nav-brand) .nav-brand img,
    [data-testid="stColumn"]:has(.nav-brand) .nav-brand img {
        pointer-events: none;
    }
    .st-key-nav_logo_home {
        position: absolute !important;
        inset: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 10 !important;
        pointer-events: auto !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .st-key-nav_logo_home .stButton,
    .st-key-nav_logo_home [data-testid="stButton"] {
        position: absolute !important;
        inset: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .st-key-nav_logo_home .stButton > button,
    .st-key-nav_logo_home button {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        outline: none !important;
        color: transparent !important;
        width: 100% !important;
        height: 100% !important;
        min-height: 100px !important;
        opacity: 0 !important;
        cursor: pointer !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        pointer-events: auto !important;
    }

    /* ══════════════════════════════════════════
       CLICKABLE USER BADGE
       The user-badge-marker sits in the same Streamlit column as the
       badge HTML and an invisible st.button that triggers st.switch_page
       to the profile. We overlay the button on top of the badge so the
       whole badge surface is clickable. Targets the .st-key-nav_user_badge
       container class added by Streamlit for the keyed widget.
    ══════════════════════════════════════════ */
    [data-testid="column"]:has(.user-badge-marker),
    [data-testid="stColumn"]:has(.user-badge-marker) {
        position: relative;
    }
    [data-testid="column"]:has(.user-badge-marker) .nav-user,
    [data-testid="stColumn"]:has(.user-badge-marker) .nav-user {
        cursor: pointer;
    }
    .st-key-nav_user_badge {
        position: absolute !important;
        inset: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 5 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .st-key-nav_user_badge .stButton,
    .st-key-nav_user_badge [data-testid="stButton"] {
        position: absolute !important;
        inset: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .st-key-nav_user_badge .stButton > button,
    .st-key-nav_user_badge button {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        outline: none !important;
        color: transparent !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }

    /* ══════════════════════════════════════════
       HOME SEARCH
    ══════════════════════════════════════════ */
    .home-search-label {
        font-size: 17px;
        font-weight: 700;
        color: #111;
        margin-bottom: 12px;
    }
    /* Form submit button in search - larger */
    [data-testid="stFormSubmitButton"] > button {
        height: 46px !important;
        font-size: 15px !important;
    }
    </style>
    """
