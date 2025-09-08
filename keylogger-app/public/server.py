from flask import Flask, request, send_file, redirect, jsonify
from flask_socketio import SocketIO
import os
from datetime import datetime

app = Flask(__name__, static_folder="public", static_url_path="/")
socketio = SocketIO(app, cors_allowed_origins="*")

PORT = 3000
LOGS_DIR = "logs"

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


def ymd():
    return datetime.now().strftime("%Y-%m-%d")


def daily_words_path():
    return os.path.join(LOGS_DIR, f"input_log_{ymd()}.txt")


# ===== API: שמירת מילה =====
@app.route("/save-input", methods=["POST"])
def save_input():
    data = request.get_json(force=True)
    user_id = str(data.get("userId", "anon")).strip()
    word = str(data.get("word", "")).strip()
    newline = bool(data.get("newline", False))

    if not word:
        return "⚠️ מילה ריקה - לא נשמרה", 400

    sep = "\n" if newline else " "
    try:
        with open(daily_words_path(), "a", encoding="utf-8") as f:
            f.write(f"[{user_id}] {word}{sep}")
    except Exception as e:
        print("❌ write error:", e)
        return "❌ שגיאה בכתיבה לקובץ. בדוק הרשאות או מקום פנוי בדיסק.", 500

    # socketio.emit("word", {"userId": user_id, "word": word, "ts": datetime.now().timestamp(), "newline": newline})
    # return "", 200


# ===== API: הורדה =====
@app.route("/download")
def download():
    fp = daily_words_path()
    if not os.path.exists(fp):
        return "⚠️ אין קובץ להיום", 404
    return send_file(fp, as_attachment=True)


# ===== דף בית =====
@app.route("/")
def home():
    return redirect("/index.html")


# ---- ניהול משתמשים מחוברים ----
online_users = {}

@socketio.on("connect")
def handle_connect():
    print("🔌 client connected:", request.sid)


@socketio.on("setUserId")
def handle_set_user_id(user_id):
    online_users[request.sid] = user_id
    broadcast_users()


@socketio.on("disconnect")
def handle_disconnect():
    if request.sid in online_users:
        del online_users[request.sid]
    broadcast_users()


def broadcast_users():
    users = list(online_users.values())
    socketio.emit("usersOnline", users)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=PORT)
