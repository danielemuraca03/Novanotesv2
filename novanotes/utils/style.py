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
    .main .block-container {
        padding-top: 72px !important;
        padding-bottom: 4rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1400px !important;
    }

    /* ─── Remove Streamlit chrome ─── */
    #MainMenu, footer { visibility: hidden; }
    /* Keep overflow visible so the sidebar collapsed control can escape the zero-height header */
    header[data-testid="stHeader"] { visibility: hidden; height: 0; overflow: visible !important; }

    /* Restore the sidebar re-open toggle — sits inside the fixed navbar strip */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        height: 64px !important;
        padding: 0 14px !important;
        z-index: 1001 !important;
        background: transparent !important;
    }
    /* Make every descendant of the toggle visible too (overrides inherited visibility:hidden from header) */
    [data-testid="stSidebarCollapsedControl"] *,
    [data-testid="collapsedControl"] * {
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* ══════════════════════════════════════════
       SIDEBAR
    ══════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: #1a1a2e;
    }
    [data-testid="stSidebar"] * {
        color: #b0b0c8 !important;
    }
    /* Brand text overrides */
    [data-testid="stSidebar"] .sidebar-brand {
        color: #ffffff !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        display: block;
    }
    [data-testid="stSidebar"] .sidebar-tagline {
        color: #5c5c88 !important;
        font-size: 12px !important;
        display: block;
        margin-top: 3px;
    }
    [data-testid="stSidebar"] .sidebar-user {
        color: #e0e0f0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.07) !important;
        margin: 0.8rem 0 !important;
    }
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        color: #b0b0c8 !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        font-size: 13px !important;
        padding: 0.35rem 0.75rem !important;
        transition: background 0.15s !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.11) !important;
        border-color: rgba(255,255,255,0.16) !important;
        color: #e0e0f0 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    /* Sidebar points badge */
    [data-testid="stSidebar"] .points-badge {
        background: rgba(0,171,107,0.15) !important;
        color: #00cc80 !important;
        border-color: rgba(0,171,107,0.28) !important;
    }
    /* Active page nav item */
    [data-testid="stSidebarNavItems"] [aria-selected="true"] span {
        color: #00cc80 !important;
    }
    [data-testid="stSidebarNavItems"] a {
        border-radius: 6px;
        transition: background 0.15s;
    }
    [data-testid="stSidebarNavItems"] a:hover {
        background: rgba(255,255,255,0.06) !important;
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
       FIXED FULL-WIDTH NAVBAR
       Identified by the NovaNotes home link (a[href="/"])
       inside the st.columns() stHorizontalBlock.
    ══════════════════════════════════════════ */

    /* Hide the nav-marker placeholder */
    .nav-marker {
        display: none !important;
    }

    /* Make the navbar columns row a fixed full-width bar */
    [data-testid="stHorizontalBlock"]:has(a[href="/"]) {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100vw !important;
        max-width: 100vw !important;
        height: 64px !important;
        z-index: 999 !important;
        background: white !important;
        border-bottom: 1px solid #e8e8e8 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        padding: 0 32px !important;
        display: flex !important;
        align-items: center !important;
        gap: 0 !important;
    }

    /* First column (logo): flush left, offset right of the sidebar toggle (~48px) */
    [data-testid="stHorizontalBlock"]:has(a[href="/"]) > [data-testid="column"]:first-child {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding: 0 0 0 48px !important;
    }

    /* Last column (login/user): flush right */
    [data-testid="stHorizontalBlock"]:has(a[href="/"]) > [data-testid="column"]:last-child {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
        padding: 0 !important;
    }

    /* Strip default page-link chrome */
    [data-testid="stPageLink"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stPageLink"] p {
        margin: 0 !important;
        line-height: 1 !important;
    }

    /* Logo link */
    [data-testid="stPageLink"] a[href="/"] {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #111 !important;
        text-decoration: none !important;
        letter-spacing: -0.4px !important;
    }
    [data-testid="stPageLink"] a[href="/"]:hover {
        color: #00ab6b !important;
        text-decoration: none !important;
    }

    /* Login button */
    [data-testid="stPageLink"] a[href*="Login"] {
        background: #00ab6b !important;
        color: white !important;
        padding: 10px 26px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        text-decoration: none !important;
        display: inline-block !important;
        line-height: 1.5 !important;
    }
    [data-testid="stPageLink"] a[href*="Login"]:hover {
        background: #009960 !important;
        color: white !important;
        text-decoration: none !important;
    }

    /* Right-align the login wrapper */
    .nav-login-wrap {
        text-align: right;
        width: 100%;
    }
    .nav-login-wrap [data-testid="stPageLink"] {
        display: inline-block !important;
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
    /* Cap the search + content width for readability on very wide viewports */
    [data-testid="stForm"] {
        max-width: 900px;
    }
    /* Form submit button in search - larger */
    [data-testid="stFormSubmitButton"] > button {
        height: 46px !important;
        font-size: 15px !important;
    }
    </style>
    """
