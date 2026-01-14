from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory, abort, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import sys
import shutil
import tempfile # For creating temporary zip files

app = Flask(__name__)
app.secret_key = "change-this-to-something-wild-drac"

# --- Configuration ---
DB_NAME = "users.db"

# DEFAULT: If you don't provide a folder argument, we use 'uploads'
BASE_DIR = os.path.abspath("uploads")

if len(sys.argv) > 1:
    target_dir = sys.argv[1]
    if os.path.exists(target_dir):
        BASE_DIR = os.path.abspath(target_dir)
        print(f" [SYSTEM] Hosting Directory: {BASE_DIR}")
    else:
        print(f" [ERROR] Directory '{target_dir}' not found. Falling back to default.")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# --- Database System ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

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

@app.route("/dashboard", defaults={'req_path': ''})
@app.route("/dashboard/<path:req_path>")
@login_required
def dashboard(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)
    
    # Security Check
    if not os.path.commonprefix([abs_path, BASE_DIR]) == BASE_DIR:
        return abort(404)

    # If it's a file, we usually download it, but let's keep the dashboard logic purely for navigation here
    if os.path.isfile(abs_path):
         return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

    if not os.path.exists(abs_path):
        return abort(404)

    items = os.listdir(abs_path)
    folders = []
    files = []
    
    for item in items:
        item_path = os.path.join(abs_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)

    parent = os.path.dirname(req_path) if req_path else None

    return render_template("dashboard.html", 
                           user=session["username"], 
                           folders=folders, 
                           files=files, 
                           current_path=req_path,
                           parent=parent)

@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    current_path = request.form.get("current_path", "")
    target_dir = os.path.join(BASE_DIR, current_path)

    if not os.path.commonprefix([target_dir, BASE_DIR]) == BASE_DIR:
        return abort(403)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if 'file' not in request.files:
        return redirect(url_for('dashboard', req_path=current_path))
    
    files = request.files.getlist('file')
    
    for file in files:
        if file.filename == '':
            continue
        
        file_path_parts = file.filename.split('/')
        safe_parts = [secure_filename(part) for part in file_path_parts]
        safe_rel_path = os.path.join(*safe_parts)
        full_dest_path = os.path.join(target_dir, safe_rel_path)
        
        os.makedirs(os.path.dirname(full_dest_path), exist_ok=True)
        file.save(full_dest_path)

    return redirect(url_for('dashboard', req_path=current_path))

# --- RETRIEVAL PROTOCOLS (Download) ---
@app.route("/retrieve", methods=["POST"])
@login_required
def retrieve_item():
    current_path = request.form.get("current_path", "")
    item_name = request.form.get("item_name")
    
    target_path = os.path.join(BASE_DIR, current_path, item_name)
    
    # Security: Stay inside BASE_DIR
    if not os.path.commonprefix([target_path, BASE_DIR]) == BASE_DIR:
        abort(403)

    if not os.path.exists(target_path):
        abort(404)

    # 1. If it's a FILE, just send it
    if os.path.isfile(target_path):
        return send_from_directory(os.path.dirname(target_path), os.path.basename(target_path), as_attachment=True)
    
    # 2. If it's a FOLDER, zip it first
    elif os.path.isdir(target_path):
        # Create a temp directory to store the zip
        temp_dir = tempfile.mkdtemp()
        try:
            # Create zip file name (e.g., MyFolder.zip)
            zip_name = f"{item_name}"
            zip_path = os.path.join(temp_dir, zip_name)
            
            # Make the archive (shutil automatically adds .zip extension)
            shutil.make_archive(zip_path, 'zip', target_path)
            
            # Send the zip file
            return send_file(f"{zip_path}.zip", as_attachment=True, download_name=f"{item_name}.zip")
        except Exception as e:
            print(f"Error zipping: {e}")
            abort(500)
            
    return redirect(url_for('dashboard', req_path=current_path))

# --- DESTRUCTION PROTOCOLS ---
@app.route("/delete", methods=["POST"])
@login_required
def delete_item():
    current_path = request.form.get("current_path", "")
    item_name = request.form.get("item_name")
    target_path = os.path.join(BASE_DIR, current_path, item_name)
    
    if not os.path.commonprefix([target_path, BASE_DIR]) == BASE_DIR:
        abort(403)
        
    if os.path.exists(target_path):
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
        else:
            os.remove(target_path)
            
    return redirect(url_for('dashboard', req_path=current_path))

@app.route("/delete-all", methods=["POST"])
@login_required
def delete_all():
    current_path = request.form.get("current_path", "")
    target_dir = os.path.join(BASE_DIR, current_path)

    if not os.path.commonprefix([target_dir, BASE_DIR]) == BASE_DIR:
        abort(403)
        
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

    return redirect(url_for('dashboard', req_path=current_path))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)