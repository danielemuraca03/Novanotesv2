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

# 4. Run the app
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
│   ├── 1_Login.py          ← Registration + login
│   ├── 2_Browse.py         ← Search, filter, download notes
│   ├── 3_Upload.py         ← Upload notes, earn points
│   ├── 4_Reviews.py        ← Course & teacher reviews
│   ├── 5_Profile.py        ← User profile, points history, leaderboard
│   └── 6_Admin.py          ← Moderation panel (admin only)
├── utils/
│   ├── navbar.py           ← Top navigation bar
│   └── style.py            ← Custom CSS
└── uploads/                ← Stored files (gitignored)
```

## Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the main file
4. Deploy!

> ⚠️ SQLite and uploaded files reset when Streamlit Cloud restarts.
> For a persistent demo, consider replacing SQLite with [Supabase](https://supabase.com) (free PostgreSQL).
