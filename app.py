# app.py
import os
import uuid
import json
import time
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, jsonify, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LAST_ACTIVE = os.path.join(DATA_DIR, "last_active.txt")
QUESTION_FILE = os.path.join(DATA_DIR, "questions.json")
PROFILE_CSV = os.getenv("PROFILE_CSV", "profile.csv")

# ensure profiles.csv exists
if not os.path.exists(PROFILES_CSV):
    df = pd.DataFrame(columns=["profile_id", "name", "gender", "age", "most_choice", "created_at"])
    df.to_csv(PROFILES_CSV, index=False)

# ensure questions.json exists (we'll create a sample if missing)
if not os.path.exists(QUESTION_FILE):
    sample_questions = [
        {"question": "What is your dominant preference for taste?", "options": ["Sweet", "Sour", "Bitter"]},
        {"question": "Which activity do you prefer?", "options": ["Sleeping", "Running", "Reading"]},
        {"question": "Choose an environment:", "options": ["Dry", "Hot", "Cold"]}
    ]
    with open(QUESTION_FILE, "w") as f:
        json.dump(sample_questions, f, indent=2)

def set_last_active(profile_id):
    with open(LAST_ACTIVE, "w") as f:
        f.write(f"{profile_id}\n{int(time.time())}")

def get_last_active(max_age_seconds=3600*6):
    # returns profile_id or None (only if last active file exists and is recent)
    if not os.path.exists(LAST_ACTIVE):
        return None
    try:
        with open(LAST_ACTIVE, "r") as f:
            pid = f.readline().strip()
            ts = int(f.readline().strip() or 0)
        if time.time() - ts > max_age_seconds:
            return None
        return pid
    except Exception:
        return None

def save_profile_row(profile):
    df = pd.read_csv(PROFILES_CSV)
    df = df.append(profile, ignore_index=True)
    df.to_csv(PROFILES_CSV, index=False)

def update_profile_most_choice(profile_id, most_choice):
    df = pd.read_csv(PROFILES_CSV)
    df.loc[df['profile_id'] == profile_id, 'most_choice'] = most_choice
    df.to_csv(PROFILES_CSV, index=False)

@app.route("/")
def index():
    profiles = pd.read_csv(PROFILES_CSV).to_dict(orient='records')
    return render_template("index.html", profiles=profiles)

@app.route("/questions_json")
def questions_json():
    return send_file(QUESTION_FILE, mimetype='application/json')

@app.route("/new_profile", methods=["GET","POST"])
def new_profile():
    if request.method == "GET":
        # show new user form (will request questions.json via client JS)
        return render_template("new_profile.html")
    data = request.form
    name = data.get("name","").strip()
    gender = data.get("gender","")
    age = data.get("age","")
    # choices submitted as JSON string
    choices_json = data.get("choices","[]")
    try:
        choices = json.loads(choices_json)
    except:
        choices = []
    # compute most chosen option (a/b/c) index 0/1/2
    counts = {"a":0, "b":0, "c":0}
    for sel in choices:
        if sel in ["a","b","c"]:
            counts[sel]+=1
    most = max(counts, key=lambda k: counts[k])
    profile_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    profile = {
        "profile_id": profile_id,
        "name": name,
        "gender": gender,
        "age": age,
        "most_choice": most,
        "created_at": created_at
    }
    save_profile_row(profile)
    # create an empty excel for this profile where ESP32 data will go
    df = pd.DataFrame(columns=["timestamp","ir1","ir2","ir3","bpm","spo2","temp","processed_label"])
    excel_path = os.path.join(DATA_DIR, f"profile_{profile_id}.xlsx")
    df.to_excel(excel_path, index=False)
    set_last_active(profile_id)
    return redirect(url_for('profile_view', profile_id=profile_id))

@app.route("/select_profile", methods=["POST"])
def select_profile():
    profile_id = request.form.get("profile_id")
    set_last_active(profile_id)
    return redirect(url_for('profile_view', profile_id=profile_id))

@app.route("/profile/<profile_id>")
def profile_view(profile_id):
    # load profile data
    profiles = pd.read_csv(PROFILES_CSV)
    row = profiles[profiles['profile_id']==profile_id]
    if row.empty:
        return "Profile not found", 404
    profile = row.iloc[0].to_dict()
    excel_path = os.path.join(DATA_DIR, f"profile_{profile_id}.xlsx")
    df = pd.DataFrame()
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
    # create waveform graphs if data exists
    graph_url = None
    if not df.empty:
        # plot IR1,IR2,IR3 and bpm
        plt.figure(figsize=(8,3))
        plt.plot(df['timestamp'], df['ir1'], label='IR1')
        plt.plot(df['timestamp'], df['ir2'], label='IR2', alpha=0.7)
        plt.plot(df['timestamp'], df['ir3'], label='IR3', alpha=0.7)
        plt.legend(loc='upper right', fontsize='small')
        plt.tight_layout()
        graph_file = os.path.join(DATA_DIR, f"graph_{profile_id}.png")
        plt.savefig(graph_file)
        plt.close()
        graph_url = url_for('static_file', path=f"data/graph_{profile_id}.png")
    return render_template("profile.html", profile=profile, data=df.to_dict(orient='records'), graph_url=graph_url)

@app.route("/static/<path:path>")
def static_file(path):
    return send_file(path)

@app.route("/esp32/data", methods=["POST"])
def esp32_data():
    """
    ESP32 will POST JSON like:
    {
      "ir1": 12345,
      "ir2": 23456,
      "ir3": 34567,
      "spo2": 95.3,
      "bpm": 72,
      "temp": 98.6,
      "processed_label": "Kapha",
      "timestamp": 1690000000
    }
    """
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({"error":"no json"}), 400
    # assign to last active profile
    profile_id = get_last_active()
    if profile_id is None:
        return jsonify({"error":"no active profile"}), 400
    excel_path = os.path.join(DATA_DIR, f"profile_{profile_id}.xlsx")
    if not os.path.exists(excel_path):
        # create if missing
        df0 = pd.DataFrame(columns=["timestamp","ir1","ir2","ir3","bpm","spo2","temp","processed_label"])
        df0.to_excel(excel_path, index=False)

    # normalize and append
    df = pd.read_excel(excel_path)
    ts = payload.get("timestamp", time.time())
    try:
        ts_iso = datetime.utcfromtimestamp(float(ts)).isoformat()
    except:
        ts_iso = datetime.utcnow().isoformat()
    row = {
        "timestamp": ts_iso,
        "ir1": payload.get("ir1"),
        "ir2": payload.get("ir2"),
        "ir3": payload.get("ir3"),
        "bpm": payload.get("bpm"),
        "spo2": payload.get("spo2"),
        "temp": payload.get("temp"),
        "processed_label": payload.get("processed_label")
    }
    df = df.append(row, ignore_index=True)
    df.to_excel(excel_path, index=False)
    return jsonify({"status":"ok", "profile_id": profile_id})

@app.route("/download_profile/<profile_id>")
def download_profile(profile_id):
    excel_path = os.path.join(DATA_DIR, f"profile_{profile_id}.xlsx")
    if os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True)
    return "No data", 404

if __name__ == "__main__":
    app.run(host=os.getenv("FLASK_HOST"),
            port=int(os.getenv("FLASK_PORT"),
            debug=os.getenv("DEBUG", "True") == "True"))
