from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory, abort, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import sys
import shutil
import tempfile
import time

app = Flask(__name__)
app.secret_key = "change-this-to-something-wild-drac"

# --- Configuration ---
DB_NAME = "users.db"
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
    # Users Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    # Metadata Table (Tracks who uploaded what)
    c.execute("""
        CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT,
            filename TEXT,
            uploader TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Helpers ---
def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def save_metadata(rel_path, filename, uploader):
    try:
        conn = get_db()
        # Remove old entry if it exists (overwrite logic)
        conn.execute("DELETE FROM file_metadata WHERE filepath=? AND filename=?", (rel_path, filename))
        conn.execute("INSERT INTO file_metadata (filepath, filename, uploader) VALUES (?, ?, ?)", 
                     (rel_path, filename, uploader))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Metadata Error: {e}")

def get_metadata_map(rel_path):
    conn = get_db()
    rows = conn.execute("SELECT filename, uploader FROM file_metadata WHERE filepath=?", (rel_path,)).fetchall()
    conn.close()
    return {row['filename']: row['uploader'] for row in rows}

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
    
    if not os.path.commonprefix([abs_path, BASE_DIR]) == BASE_DIR:
        return abort(404)

    if os.path.isfile(abs_path):
         return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

    if not os.path.exists(abs_path):
        return abort(404)

    # Get Metadata for this folder
    meta_map = get_metadata_map(req_path)

    items = os.listdir(abs_path)
    folders = []
    files = []
    
    for item in items:
        # Hide the temporary partial files from the view
        if item.endswith(".part"):
            continue

        item_path = os.path.join(abs_path, item)
        uploader = meta_map.get(item, "Unknown") # Default to Unknown if not in DB

        if os.path.isdir(item_path):
            folders.append({'name': item, 'uploader': uploader})
        else:
            files.append({'name': item, 'uploader': uploader})

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
    uploader = session["username"]
    
    for file in files:
        if file.filename == '':
            continue
        
        file_path_parts = file.filename.split('/')
        safe_parts = [secure_filename(part) for part in file_path_parts]
        safe_rel_path = os.path.join(*safe_parts)
        full_dest_path = os.path.join(target_dir, safe_rel_path)
        
        # Determine the directory of the file (for metadata relative path)
        file_dir_rel = os.path.dirname(safe_rel_path)
        # If it's a folder upload, we want to tag the root folder? 
        # Actually, let's just tag the file itself.
        # But we need to store metadata relative to the dashboard view.
        # If I upload Folder/File.txt, dashboard at / sees "Folder".
        # Let's tag the specific file.
        # Ideally, we tag the root folder too.
        
        # 1. ATOMIC SAVE PROTOCOL
        temp_path = full_dest_path + ".part"
        
        try:
            os.makedirs(os.path.dirname(full_dest_path), exist_ok=True)
            file.save(temp_path)
            
            # If we reached here, upload is complete and valid.
            # Rename .part to real name
            if os.path.exists(full_dest_path):
                os.remove(full_dest_path) # Overwrite existing
            os.rename(temp_path, full_dest_path)
            
            # 2. METADATA TAGGING
            # We tag the file itself
            # We need the relative path of the file w.r.t BASE_DIR + current_path?
            # No, w.r.t the folder it sits in.
            
            # For the dashboard to see it:
            # If I am at /dashboard/Sub, and file is at /Sub/file.txt
            # DB needs: filepath="Sub", filename="file.txt"
            
            # Calculate where this file lives relative to BASE_DIR
            actual_rel_dir = os.path.join(current_path, os.path.dirname(safe_rel_path))
            # Normalize path separators
            actual_rel_dir = actual_rel_dir.replace("\\", "/").strip("/")
            
            save_metadata(actual_rel_dir, os.path.basename(full_dest_path), uploader)

            # Also tag the top-level folder if it's a folder upload
            if len(safe_parts) > 1:
                top_folder = safe_parts[0]
                save_metadata(current_path, top_folder, uploader)

        except Exception as e:
            print(f"Upload Failed: {e}")
            # CLEANUP CORRUPTED FILE
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return redirect(url_for('dashboard', req_path=current_path))

@app.route("/retrieve", methods=["POST"])
@login_required
def retrieve_item():
    current_path = request.form.get("current_path", "")
    item_name = request.form.get("item_name")
    
    target_path = os.path.join(BASE_DIR, current_path, item_name)
    
    if not os.path.commonprefix([target_path, BASE_DIR]) == BASE_DIR:
        abort(403)

    if not os.path.exists(target_path):
        abort(404)

    if os.path.isfile(target_path):
        return send_from_directory(os.path.dirname(target_path), os.path.basename(target_path), as_attachment=True)
    
    elif os.path.isdir(target_path):
        temp_dir = tempfile.mkdtemp()
        try:
            zip_name = f"{item_name}"
            zip_path = os.path.join(temp_dir, zip_name)
            shutil.make_archive(zip_path, 'zip', target_path)
            return send_file(f"{zip_path}.zip", as_attachment=True, download_name=f"{item_name}.zip")
        except Exception as e:
            abort(500)
            
    return redirect(url_for('dashboard', req_path=current_path))

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
            
        # DELETE METADATA
        conn = get_db()
        conn.execute("DELETE FROM file_metadata WHERE filepath=? AND filename=?", (current_path, item_name))
        conn.commit()
        conn.close()
            
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
        
        # Wipe metadata for this sector
        conn = get_db()
        conn.execute("DELETE FROM file_metadata WHERE filepath=?", (current_path,))
        conn.commit()
        conn.close()

    return redirect(url_for('dashboard', req_path=current_path))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)