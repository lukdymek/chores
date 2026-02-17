# Family Chores (Django + SQLite)

Simple website for 4 users (Alex, Olivia, Olga, Lukas) to manage daily chores.

## Features
- Login for each family member.
- Daily chores shown per user.
- Users can mark their own chores as `Done` / `Undo`.
- Lukas is the admin and can add chores for any user.
- Upload completion photos from mobile (up to 3 images per task).
- Admin panel available at `/admin/` for Lukas.
- SQLite database by default.

## Default users
Users are auto-created during migration:
- `alex`
- `olivia`
- `olga`
- `lukas` (admin)

Default password format: `username12345` (example: `alex12345`).

Change all passwords after first login.

## Local run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Railway deployment
1. Push this project to GitHub.
2. Create a new Railway project from the repo.
3. Set env vars in Railway:
   - `SECRET_KEY` = long random string
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = your Railway domain (comma-separated if multiple)
   - `CSRF_TRUSTED_ORIGINS` = `https://your-domain.up.railway.app`
4. Deploy.

Railway uses `Procfile` (`gunicorn chores_project.wsgi`).

## Note on uploads
Task photos are stored in `/media`. With SQLite and local disk, uploaded files are not durable if Railway restarts or redeploys. Later, move media storage to cloud object storage (for example S3-compatible) for persistence.
