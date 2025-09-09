# from flask import Flask, jsonify, request , redirect
# from flask_cors import CORS
# import json

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Initial computers data
# computers = [
#     {
#         "mac_address": "00:1A:2B:3C:4D:5E",
#         "name": "חסן נסראללה",
#         "address": "לבנון",
#     },
#     {
#         "mac_address": "A4:5E:60:9B:3F:1D",
#         "name": "יחיא סינואר",
#         "address": "רצועת עזה",
#     },
#     {
#         "mac_address": "F0:D5:BF:12:34:56",
#         "name": "חמינאי",
#         "address": "איראן",
#     }
# ]

# @app.route('/')
# def index():
#     return redirect('/static/index.html')

# # Get all computers (name and MAC_address only)
# @app.route('/api/computers', methods=['GET'])
# def get_computers():
#     simplified_computers = [{"mac_address": computer["mac_address"], "name": computer["name"]} for computer in computers]
#     print(f'{simplified_computers}')
#     return jsonify(simplified_computers)


# # Get specific computer details
# @app.route('/api/computers/<computer_mac_address>', methods=['GET'])
# def get_computer(computer_mac_address):
#     computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)
#     if computer:
#         return jsonify(computer)
#     else:
#         return jsonify({"error": "מחשב לא נמצא"}), 404


# # Add new computer
# @app.route('/api/computers', methods=['POST'])
# def add_computer():
#     new_computer = request.json

#     # Check if computer with this MAC_address already exists
#     if any(c["mac_address"] == new_computer["mac_address"] for c in computers):
#         return jsonify({"error": "מחשב עם כתובת mac זו כבר קיים"}), 400

#     # Add new computer
#     computers.append(new_computer)
#     return jsonify(new_computer), 201


# # Update computer details
# @app.route('/api/computers/<computer_mac_address>', methods=['PUT'])
# def update_computer(computer_mac_address):
#     update_data = request.json
#     computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)

#     if not computer:
#         return jsonify({"error": "מחשב לא נמצא"}), 404

#     # Update computer fields
#     if "name" in update_data:
#         computer["name"] = update_data["name"]
#     if "address" in update_data:
#         computer["address"] = update_data["address"]

#     return jsonify(computer)


# if __name__ == '__main__':
#     app.run(debug=True)



    # lines = 80-94 # Add grade to computer
# @app.route('/api/computers/<computer_mac_address>/grades', methods=['POST'])
# def add_grade(computer_mac_address):
#     grade_data = request.json
#     computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)

#     if not computer:
#         return jsonify({"error": "מחשב לא נמצא"}), 404

#     if "grade" not in grade_data:
#         return jsonify({"error": "נתון הציון חסר"}), 400

#     # Add new grade
#     computer["grades"].append(grade_data["grade"])
#     return jsonify(computer)




# # my project version 2
# from flask import Flask, jsonify, request, redirect
# from flask_cors import CORS
# import json

# app = Flask(__name__)
# CORS(app)

# # ---------- קריאה/שמירה לקובץ JSON ----------
# def save_data():
#     with open('computers.json', 'w', encoding='utf-8') as f:
#         json.dump(computers, f, ensure_ascii=False, indent=4)

# def load_data():
#     global computers
#     try:
#         with open('computers.json', 'r', encoding='utf-8') as f:
#             computers = json.load(f)
#     except FileNotFoundError:
#         computers = [ {
#         "mac_address": "00:1A:2B:3C:4D:5E",
#         "name": "חסן נסראללה",
#         "address": "לבנון",
#     },
#     {
#         "mac_address": "A4:5E:60:9B:3F:1D",
#         "name": "יחיא סינואר",
#         "address": "רצועת עזה",
#     },
#     {
#         "mac_address": "F0:D5:BF:12:34:56",
#         "name": "חמינאי",
#         "address": "איראן",
#     }]
# # טען את הנתונים מהקובץ (לפני שמתחילים לעבוד עם המידע)
# load_data()
# # -------------------------------------------------

# @app.route('/')
# def index():
#     return redirect('/static/index.html')

# @app.route('/api/computers', methods=['GET'])
# def get_computers():
#     simplified_computers = [{"mac_address": c["mac_address"], "name": c["name"]} for c in computers]
#     return jsonify(simplified_computers)

# @app.route('/api/computers/<computer_mac_address>', methods=['GET'])
# def get_computer(computer_mac_address):
#     computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)
#     if computer:
#         return jsonify(computer)
#     else:
#         return jsonify({"error": "מחשב לא נמצא"}), 404

# @app.route('/api/computers', methods=['POST'])
# def add_computer():
#     new_computer = request.json
#     if any(c["mac_address"] == new_computer["mac_address"] for c in computers):
#         return jsonify({"error": "מחשב עם כתובת mac זו כבר קיים"}), 400

#     computers.append(new_computer)
#     save_data()  # 🔸 שמירה אחרי הוספה
#     return jsonify(new_computer), 201

# @app.route('/api/computers/<computer_mac_address>', methods=['PUT'])
# def update_computer(computer_mac_address):
#     update_data = request.json
#     computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)

#     if not computer:
#         return jsonify({"error": "מחשב לא נמצא"}), 404

#     if "name" in update_data:
#         computer["name"] = update_data["name"]
#     if "address" in update_data:
#         computer["address"] = update_data["address"]

#     save_data()  # 🔸 שמירה אחרי עדכון
#     return jsonify(computer)

# if __name__ == '__main__':
#     app.run(debug=True)




# server/app.py


# from flask import Flask, jsonify, request, abort ,redirect
# import os
# from datetime import datetime

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return redirect('/static/index.html')

# # נתיב בסיס לתיקיית הלוגים שלך (ששם הקילוגר שומר את הקבצים)
# BASE_LOG_DIR = "C:/Users/יוסף יצחק אוחיון/Desktop/קודקוד/fullstack/פרויקטים/keylogger/KeyLogger/backend"


# def get_log_files(mac_address, from_datetime, to_datetime):
#     """
#     מקבל כתובת MAC, טווח זמן ומחזיר רשימה של קבצי לוג מתאימים.
#     """
#     folder_path = os.path.join(BASE_LOG_DIR, mac_address)
#     if not os.path.exists(folder_path):
#         return None  # תיקיה לא קיימת

#     log_files = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.txt'):
#             # נניח שהשם בפורמט "dd-mm-yy_HH.txt"
#             try:
#                 file_datetime = datetime.strptime(filename[:-4], "%d-%m-%y_%H")
#                 if from_datetime <= file_datetime <= to_datetime:
#                     log_files.append(os.path.join(folder_path, filename))
#             except ValueError:
#                 pass  # אם שם הקובץ לא תואם לפורמט, נתעלם

#     return sorted(log_files)

# @app.route('/api/logs', methods=['GET'])
# def get_logs():
#     mac = request.args.get('mac')
#     from_date = request.args.get('from_date')  # בפורמט "dd-mm-yy"
#     from_hour = request.args.get('from_hour')  # בפורמט מספר 0-23
#     to_date = request.args.get('to_date')
#     to_hour = request.args.get('to_hour')

#     if not all([mac, from_date, from_hour, to_date, to_hour]):
#         return jsonify({"error": "Missing required parameters"}), 400

#     try:
#         from_dt = datetime.strptime(f"{from_date}_{int(from_hour):02d}", "%d-%m-%y_%H")
#         to_dt = datetime.strptime(f"{to_date}_{int(to_hour):02d}", "%d-%m-%y_%H")
#     except ValueError:
#         return jsonify({"error": "Invalid date or hour format"}), 400

#     log_files = get_log_files(mac, from_dt, to_dt)
#     if log_files is None:
#         return jsonify({"error": "מחשב לא נמצא"}), 404

#     logs_content = ""
#     for filepath in log_files:
#         with open(filepath, 'r', encoding='utf-8') as f:
#             logs_content += f.read() + "\n"

#     return jsonify({"logs": logs_content})

# if __name__ == '__main__':
#     app.run(debug=True)



import re
from flask import Flask, jsonify, request, abort ,redirect
import os
from datetime import datetime

app = Flask(__name__)

BASE_LOG_DIR = "C:/Users/יוסף יצחק אוחיון/Desktop/קודקוד/fullstack/פרויקטים/keylogger/KeyLogger/backend/Computers"

def is_valid_mac(mac):
    return re.match(r'^[0-9A-Fa-f\-]+$', mac) is not None

def get_log_files(mac_address, from_datetime, to_datetime):
    folder_path = os.path.join(BASE_LOG_DIR, mac_address)
    if not os.path.exists(folder_path):
        return None  # תיקיה לא קיימת

    log_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            try:
                file_datetime = datetime.strptime(filename[:-4], "%d-%m-%y_%H")
                if from_datetime <= file_datetime <= to_datetime:
                    log_files.append(os.path.join(folder_path, filename))
            except ValueError:
                pass

    return sorted(log_files)

def read_log_files(filepaths):
    logs_content = ""
    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            logs_content += f.read() + "\n"
    return logs_content

@app.route('/')
def index():
    return redirect('/static/index.html')

@app.route('/api/logs', methods=['GET'])
def get_logs():
    mac = request.args.get('mac')
    from_date = request.args.get('from_date')  # "dd-mm-yy"
    from_hour = request.args.get('from_hour')  # 0-23
    to_date = request.args.get('to_date')
    to_hour = request.args.get('to_hour')

    if not all([mac, from_date, from_hour, to_date, to_hour]):
        return jsonify({"error": "Missing required parameters"}), 400

    if not is_valid_mac(mac):
        return jsonify({"error": "Invalid MAC address format"}), 400

    try:
        from_dt = datetime.strptime(f"{from_date}_{int(from_hour):02d}", "%d-%m-%y_%H")
        to_dt = datetime.strptime(f"{to_date}_{int(to_hour):02d}", "%d-%m-%y_%H")
    except ValueError:
        return jsonify({"error": "Invalid date or hour format"}), 400

    log_files = get_log_files(mac, from_dt, to_dt)
    if log_files is None:
        return jsonify({"error": "מחשב לא נמצא"}), 404

    if not log_files:
        return jsonify({"message": "אין קבצים בטווח התאריכים שנבחר"}), 404

    logs_content = read_log_files(log_files)

    return jsonify({
        "files": [os.path.basename(fp) for fp in log_files],
        "logs": logs_content
    })

@app.route('/api/computers/', methods=['GET'])
def list_computers():
    try:
        computers = []
        for name in os.listdir(BASE_LOG_DIR):
            folder_path = os.path.join(BASE_LOG_DIR, name)
            if os.path.isdir(folder_path):
                computers.append({"mac_address": name})
        return jsonify(computers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
