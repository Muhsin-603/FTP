from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "change-this-to-something-wild-drac" 

# --- Configuration ---
DB_NAME = "users.db"
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Database System ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Simple table: Just ID, Username, and Password. No ranks.
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the system
init_db()

# --- Security Gate ---
def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# --- Routes ---

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        try:
            conn.execute("INSERT INTO users(username, password) VALUES (?,?)", (username, password))
            conn.commit()
            conn.close()
            return redirect("/")
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username already exists")
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("dashboard.html", user=session["username"], files=files)

@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return redirect("/dashboard")
    file = request.files['file']
    if file.filename == '':
        return redirect("/dashboard")
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect("/dashboard")

@app.route("/download/<filename>")
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)