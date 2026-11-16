# SnapSpace — Django REST + Flutter rebuild

This branch starts a separate full-stack implementation. The existing GitHub Pages app on main remains untouched while the replacement is built and tested.

## Architecture
- Flutter: shared Android, iOS and web client.
- Django REST Framework + SimpleJWT: API and authentication.
- PostgreSQL: primary relational database.
- Redis: reserved for caching, throttling and async jobs.
- Existing Supabase project: legacy source for profile/post/social data and media URLs during migration.

## Migration safety
- Supabase Auth password hashes cannot be reused as Django passwords. Existing users need a password reset or one-time account-claim flow.
- Preserve existing UUIDs when importing users so relationships remain intact.
- Keep Supabase Storage media URLs working initially; migrate media only after validating copies.
- Never put Django secrets, database passwords, or Supabase service-role keys in Flutter or a public repository.

## Backend setup (Windows PowerShell)
1. Install Python 3.12+, Docker Desktop and Flutter stable.
2. `cd backend`
3. `py -3.12 -m venv .venv`
4. `.\.venv\Scripts\Activate.ps1`
5. `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and set a strong local Django secret.
7. From repo root: `docker compose up -d db redis`
8. From backend: `python manage.py makemigrations social`
9. `python manage.py migrate`
10. `python manage.py createsuperuser`
11. `python manage.py runserver`
12. Health check: `http://127.0.0.1:8000/api/health/`

## Flutter setup
1. `cd mobile`
2. `flutter pub get`
3. Android emulator: `flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api`
4. Chrome: `flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8000/api`

## Current status
Starter auth, profile, feed, like/comment, follow and notification API structures are scaffolded. Flutter currently contains the starter login/feed shell. Media uploads, complete app navigation, stories, real-time chat, moderation, migration scripts, automated tests and production deployment remain next milestones. Not production-ready yet.
