# SnapSpace — browser-first rebuild

The existing public GitHub Pages app on `main` remains untouched. This branch contains the new Django-powered browser application and API.

## Browser support
The new responsive interface is served by Django at `/` and uses same-origin API requests. It is designed for current Chrome, Microsoft Edge, Firefox and Safari on desktop and mobile. Test on real devices and browsers before calling the release production-ready.

## Architecture
- Django 5.2 + Django REST Framework + SimpleJWT: web app, API and authentication.
- SQLite: quick local development without Docker.
- PostgreSQL: intended production database.
- WhiteNoise: production static assets.
- Flutter: future shared Android/iOS client (the starter remains in `mobile/`).

## Run locally on Windows (no Docker or Flutter required)
Use a separate working folder so the existing website checkout stays safe:

```powershell
cd $HOME
git clone -b django-flutter-rebuild https://github.com/Riddhima-prog/snapspace.git snapspace-browser
cd snapspace-browser\backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

For SQLite local development, open `backend/.env` and set:
- `DJANGO_SECRET_KEY`: a long random value
- `DJANGO_DEBUG=True`
- Leave `DATABASE_URL` empty or remove that line so Django uses its local SQLite database.

Then run:

```powershell
python manage.py makemigrations social
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in Chrome or Edge. API health check: `http://127.0.0.1:8000/api/health/`.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Current browser features
- Signup and login (JWT)
- Responsive dark interface with desktop sidebar and mobile navigation
- Feed, image/video posts by public media URL, likes and comments
- People search and follow
- Notifications list
- Basic profile display and editing

## Known limitations before public launch
- Media URL posting is temporary; secure direct uploads and storage limits still need implementation.
- Password reset, email verification, account recovery and refresh-token rotation flow need completion.
- Stories, Reels publishing, chat, report/block/moderation, accessibility review and richer profile controls remain future work.
- Add automated backend/frontend tests, database migrations, backups, rate limits, security headers and monitoring before production.
- Supabase data is not migrated by this branch yet. Keep the old project and media intact; plan and verify an export/import before switching users.
- Supabase Auth password hashes cannot be reused as Django passwords; existing users will need a password reset or account-claim flow.

## Deployment
Deploy the Django app and managed PostgreSQL together on a Python-compatible host. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, and `DATABASE_URL` as server-side environment variables. Never commit secrets or put database credentials in browser code. Run migrations and collect static files during deployment. Attach a custom domain only after the hosted health check succeeds.
