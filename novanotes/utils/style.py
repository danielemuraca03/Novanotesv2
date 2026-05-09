"""
NovaNotes — Custom CSS styling.
Injected via st.markdown to override Streamlit defaults.
"""


def get_custom_css():
    """Return the CSS string to inject into the app."""
    return """
    <style>
    /* ── Import a distinctive font ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&display=swap');

    /* ── Global overrides ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Sidebar styling ── */
    [data-testid="stSidebar"] {
        background: #1a1a2e;
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #a0a0b8 !important;
        font-size: 13px;
    }

    /* ── Header area ── */
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }

    /* ── Note cards ── */
    .note-card {
        background: white;
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
        transition: box-shadow 0.2s ease;
    }
    .note-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }

    /* ── Star display ── */
    .stars {
        color: #f4a261;
        font-size: 18px;
        letter-spacing: 2px;
    }
    .stars-dim {
        color: #ddd;
    }

    /* ── Points badge ── */
    .points-badge {
        background: #1a1a2e;
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 14px;
        display: inline-block;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #eee;
    }
    [data-testid="stMetric"] label {
        color: #666 !important;
        font-size: 13px !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton > button[kind="primary"] {
        background: #1a1a2e;
        color: white;
        border: none;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }

    /* ── Divider ── */
    hr {
        border: none;
        border-top: 1px solid #eee;
        margin: 1.5rem 0;
    }

    /* ── Success / warning / error boxes ── */
    .stAlert {
        border-radius: 10px;
    }

    /* ── Hide Streamlit branding (optional) ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
