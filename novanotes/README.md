# 📚 NovaNotes

A platform where Nova SBE students share class notes, study tips, and course reviews using a points-based system.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-team/novanotes.git
cd novanotes

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up secrets (for email verification)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your Gmail app password

# 5. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Project Structure

```
novanotes/
├── app.py                  ← Main entry point
├── config.py               ← Shared constants (points, email domain)
├── db.py                   ← All database functions
├── requirements.txt
├── .gitignore
├── pages/
│   ├── 1_Login.py          ← Registration + login + email verify
│   ├── 2_Browse.py         ← Search, filter, download notes
│   ├── 3_Upload.py         ← Upload notes, earn points
│   ├── 4_Reviews.py        ← Course & teacher reviews
│   ├── 5_Profile.py        ← User profile, points history, leaderboard
│   └── 6_Admin.py          ← Moderation panel (admin only)
├── utils/
│   ├── email_verify.py     ← Verification token + SMTP
│   └── style.py            ← Custom CSS
├── uploads/                ← Stored files (gitignored)
└── .streamlit/
    └── secrets.toml        ← SMTP credentials (gitignored)
```

## Team Division

| Weeks | Pair | What to build |
|-------|------|---------------|
| 1–2   | Pair 1 (A + B) | Login, registration, email verify, upload, browse, download, points engine |
| 3–4   | Pair 2 (C + D) | Reviews, profile, leaderboard, admin panel, flagging, UI polish, deploy |

## Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the main file
4. Add your secrets in the app settings (Settings → Secrets)
5. Deploy!

> ⚠️ SQLite and uploaded files reset when Streamlit Cloud restarts.
> For a persistent demo, consider replacing SQLite with [Supabase](https://supabase.com) (free PostgreSQL).
