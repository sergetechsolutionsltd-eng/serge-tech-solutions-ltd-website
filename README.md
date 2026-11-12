# SERGE TECH SOLUTIONS LTD — Website package

## Included
- Responsive website with company logo and a separate illustrative image for each listed service.
- Real enquiry form saved to a local SQLite database (not just a mailto link).
- Admin login and enquiry dashboard.
- Database download from the admin dashboard.
- SQL schema, starter database, and backup script.
- Your supplied company logo and holiday-training photo.

## Run locally (Windows / Mac / Linux)
1. Install Python 3.10 or later.
2. Extract this folder.
3. Open a terminal in this folder and run:
   `python -m venv .venv`
4. Activate the environment:
   - Windows: `.venv\\Scripts\\activate`
   - Mac/Linux: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create an admin password hash: `python make_admin_hash.py`
7. Set environment variables before starting:
   - `SECRET_KEY` to a long random secret
   - `ADMIN_USERNAME` to your chosen admin username
   - `ADMIN_PASSWORD_HASH` to the hash printed by the helper
8. Start: `python app.py`
9. Visit `http://127.0.0.1:5000`
10. Admin: `http://127.0.0.1:5000/admin/login`

The starter SQLite database is created automatically at `data/serge_tech.db` the first time the app starts.

## Backups
- Run `python backup_database.py` to create a timestamped copy in `backups/`.
- While running, sign in as administrator and use **Download database backup**.
- Keep at least one backup outside the website server (for example, a secure computer or encrypted cloud storage). Do not publish database files in the public website folder.

## Production hosting
This package uses Flask + SQLite. It needs a Python-capable host (for example a VPS or a platform that supports persistent disks). A static-only host such as GitHub Pages cannot run the enquiry backend. If deploying to a host with an ephemeral filesystem, configure a persistent disk and set `DATABASE_PATH` to that disk path, or records may be lost on redeploy/restart. Use HTTPS, strong unique admin credentials, and regular off-server backups.

## Before launch — please verify
- Company phone, WhatsApp and email details.
- Official Facebook, TikTok and YouTube profile URLs. The current links are generic platform links; replace them with the actual company profile links.
- Permission to display the project/client names.
- The service thumbnails are illustrative visual assets; replace with exact product/installation photos from your own projects when available.
- Add a separate public training-registration form if you want students/guardians to register online. The database table is prepared, but the public registration workflow is not yet enabled.
- Configure an email/SMS notification service if the company wants instant alerts for new enquiries.

## Current company contact details shown
Call: 0200 908 491
WhatsApp: +256 706 568 873
Email: sergetechsolutions@gmail.com
Location: Kampala, Uganda
