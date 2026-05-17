# 📚 NovaNotes

A Streamlit app where Nova SBE students share class notes and course reviews, with a points economy to incentivize good content (earn on upload, spend on download).

**Stack:** Streamlit · Supabase Postgres (via `psycopg2`) · bcrypt auth · Streamlit Cloud for hosting.

# Project structure

```
novanotes/
├── app.py                      ← Entry point; bootstrap (init_tables + demo admin)
├── config.py                   ← Points economy, email gate, demo admin creds
├── db.py                       ← All Postgres queries; cached reads, mutation cache-bust
├── populate_demo.py            ← One-shot demo seeder
├── pages/
│   ├── 1_Login.py              ← Login + registration (gated to @novasbe.pt)
│   ├── 2_Browse.py             ← Filter / search / download notes
│   ├── 3_Upload.py             ← Upload note file, earn points
│   ├── 4_Reviews.py            ← Browse / write course reviews
│   ├── 5_Profile.py            ← Stats, points history, leaderboard
│   └── 6_Admin.py              ← Flag triage, note deletion, user moderation
├── utils/
│   ├── navbar.py               ← Top nav with clickable logo + user badge
│   └── style.py                ← All CSS (a lot of !important for Streamlit override)
├── static/
│   ├── logo.png                ← Used in the top navbar
│   └── demo_files/             ← Bundled PDFs for demo notes
├── uploads/                    ← User-uploaded files (gitignored, ephemeral on Cloud)
└── .streamlit/
    ├── config.toml             ← Streamlit server config (max upload size)
    └── secrets.toml            ← DB + Supabase keys (gitignored, never commit)
```

## Quick start (local)

```bash
git clone https://github.com/danielemuraca03/Novanotesv2.git
cd Novanotesv2

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create `novanotes/.streamlit/secrets.toml` (gitignored) with your Supabase credentials:

```toml
DATABASE_URL = "postgresql://postgres.<project-ref>:<url-encoded-password>@aws-0-<region>.pooler.supabase.com:6543/postgres"
SUPABASE_URL = "https://<project-ref>.supabase.co"
SUPABASE_KEY = "<your-anon-key>"
```

Then run:

```bash
cd novanotes
streamlit run app.py            # opens http://localhost:8501
```

On first launch the app creates all tables and the demo admin account (`admin@novasbe.pt` / `admin123`).

### Getting the Supabase credentials

1. Create a project at [supabase.com](https://supabase.com).
2. **`DATABASE_URL`** — Project Settings → Database → "Transaction pooler" tab. Copy the URI. **Important:** any special characters in your password must be URL-encoded (`%` → `%25`, `,` → `%2C`, `/` → `%2F`, etc.).
3. **`SUPABASE_URL`** and **`SUPABASE_KEY`** — Project Settings → API. Use the base project URL (no `/rest/v1/` suffix) and the `anon` public key.

The schema is created automatically by `db.init_tables()` on first run; no manual migration needed.

## Seeding demo data

The app starts with an empty database. To populate it with realistic-looking demo content (12 student users, 7 notes, 10 ratings, 6 reviews):

```bash
cd novanotes
python populate_demo.py
```

The script is **idempotent**: re-running it upserts users by email and skips the content phase if any demo user already owns notes.

Demo notes reference PDFs bundled in `novanotes/static/demo_files/`. Drop any `.pdf` files there before running — each demo note gets a random one assigned. Since these PDFs ship with the repo, they're available both locally and on Streamlit Cloud.

To rebuild demo content from scratch, run this in the Supabase SQL editor (it preserves the admin account):

```sql
DELETE FROM ratings WHERE note_id IN (
  SELECT id FROM notes WHERE user_id IN (
    SELECT id FROM users WHERE email LIKE '%@novasbe.pt' AND email <> 'admin@novasbe.pt'
  )
);
DELETE FROM flags WHERE content_type = 'note' AND content_id IN (
  SELECT id FROM notes WHERE user_id IN (
    SELECT id FROM users WHERE email LIKE '%@novasbe.pt' AND email <> 'admin@novasbe.pt'
  )
);
DELETE FROM reviews WHERE user_id IN (
  SELECT id FROM users WHERE email LIKE '%@novasbe.pt' AND email <> 'admin@novasbe.pt'
);
DELETE FROM notes WHERE user_id IN (
  SELECT id FROM users WHERE email LIKE '%@novasbe.pt' AND email <> 'admin@novasbe.pt'
);
```

Then re-run `populate_demo.py`.

## Performance notes

`db.py` decorates all read functions with `@st.cache_data` (60s TTL for hot data, 5min for slow-changing like leaderboard / course list). Every mutation calls `_bust_cache()` so writes show up immediately. `app.py` guards the bootstrap (`init_tables` + demo admin) with a `st.session_state._bootstrap_done` flag so it runs once per session, wrapped in a spinner for the cold start.

`2_Browse.py` pre-fetches the user's ratings and points balance once before the per-note loop — important because Streamlit re-evaluates every expander body on every rerun.

## Known caveats

- **User-uploaded files (`uploads/`) don't survive a Streamlit Cloud redeploy.** The folder is on ephemeral disk; only files committed in git (like `static/demo_files/`) persist. For real production uploads you'd need to wire `3_Upload.py` and `2_Browse.py` to Supabase Storage.
- **Free-tier sleep:** both Streamlit Cloud (apps sleep after ~7 days of zero traffic) and Supabase (projects pause after ~1 week of zero DB activity) hibernate when fully idle. Both auto-wake on the next request.
- **Demo admin password is hardcoded** in `config.py` (`admin123`). Change `DEMO_ADMIN_PASSWORD` and the auto-create logic in `app.py` before any non-demo use.


