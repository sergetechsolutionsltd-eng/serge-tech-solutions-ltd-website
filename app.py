import os, sqlite3, secrets
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort
from werkzeug.security import check_password_hash, generate_password_hash

BASE = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE, "data", "serge_tech.db"))
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "CHANGE-THIS-TO-A-LONG-RANDOM-SECRET")
ADMIN_USER = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS enquiries (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL, phone TEXT NOT NULL, email TEXT,
          category TEXT NOT NULL, message TEXT,
          created_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'New'
        );
        CREATE TABLE IF NOT EXISTS training_registrations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          student_name TEXT NOT NULL, guardian_name TEXT, phone TEXT NOT NULL,
          class_level TEXT, programme TEXT, notes TEXT,
          created_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'New'
        );
        CREATE TABLE IF NOT EXISTS site_settings (
          key TEXT PRIMARY KEY, value TEXT NOT NULL
        );
        """)
        con.execute("INSERT OR IGNORE INTO site_settings(key,value) VALUES('company_name','SERGE TECH SOLUTIONS LTD')")
        con.execute("INSERT OR IGNORE INTO site_settings(key,value) VALUES('company_email','sergetechsolutions@gmail.com')")

def admin_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapped

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/enquiry")
def enquiry():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    category = request.form.get("category", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not phone or not category:
        flash("Please provide your name, phone number and enquiry type.", "error")
        return redirect(url_for("home") + "#contact")
    with db() as con:
        con.execute("""INSERT INTO enquiries(name,phone,email,category,message,created_at)
                       VALUES(?,?,?,?,?,?)""",
                    (name[:100], phone[:40], email[:120], category[:120], message[:3000],
                     datetime.now(timezone.utc).isoformat()))
    return render_template("submitted.html", title="Enquiry received",
        message="Thank you. Your enquiry has been recorded. The Serge Tech team can follow up using the contact details you supplied.")

@app.get("/admin/login")
def admin_login():
    return render_template("login.html")

@app.post("/admin/login")
def admin_login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not ADMIN_PASSWORD_HASH:
        flash("Admin password is not configured. Set ADMIN_PASSWORD_HASH in your environment first.", "error")
        return redirect(url_for("admin_login"))
    if secrets.compare_digest(username, ADMIN_USER) and check_password_hash(ADMIN_PASSWORD_HASH, password):
        session.clear()
        session["admin_logged_in"] = True
        return redirect(url_for("admin_dashboard"))
    flash("Incorrect username or password.", "error")
    return redirect(url_for("admin_login"))

@app.get("/admin")
@admin_required
def admin_dashboard():
    with db() as con:
        enquiries = con.execute("SELECT * FROM enquiries ORDER BY id DESC LIMIT 200").fetchall()
        registrations = con.execute("SELECT * FROM training_registrations ORDER BY id DESC LIMIT 200").fetchall()
    return render_template("admin.html", enquiries=enquiries, registrations=registrations)

@app.post("/admin/enquiry/<int:item_id>/status")
@admin_required
def update_enquiry(item_id):
    status = request.form.get("status", "New")
    if status not in ("New", "In progress", "Closed"):
        abort(400)
    with db() as con:
        con.execute("UPDATE enquiries SET status=? WHERE id=?", (status, item_id))
    return redirect(url_for("admin_dashboard"))

@app.get("/admin/backup")
@admin_required
def download_backup():
    if not os.path.exists(DB_PATH):
        abort(404)
    # SQLite backup API creates a consistent copy even if the live database is in use.
    backup_path = os.path.join(BASE, "data", "serge_tech_backup.sqlite3")
    source = sqlite3.connect(DB_PATH)
    target = sqlite3.connect(backup_path)
    source.backup(target)
    target.close()
    source.close()
    return send_file(backup_path, as_attachment=True, download_name="serge_tech_database_backup.sqlite3")

@app.post("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.errorhandler(404)
def not_found(error):
    return render_template("submitted.html", title="Page not found",
        message="The page you requested could not be found."), 404

init_db()

if __name__ == "__main__":
    # Local development only. For production use a WSGI server such as gunicorn.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
