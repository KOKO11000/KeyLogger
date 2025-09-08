from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initial computers data
computers = [
    {
        "mac_address": "00:1A:2B:3C:4D:5E",
        "name": "חסן נסראללה",
        "address": "לבנון",
    },
    {
        "mac_address": "A4:5E:60:9B:3F:1D",
        "name": "יחיא סינואר",
        "address": "רצועת עזה",
    },
    {
        "mac_address": "F0:D5:BF:12:34:56",
        "name": "חמינאי",
        "address": "איראן",
    }
]

@app.route('/')
def index():
    return app.redirect('/static/index.html')

# Get all computers (name and MAC_address only)
@app.route('/api/computers', methods=['GET'])
def get_computers():
    simplified_computers = [{"mac_address": computer["mac_address"], "name": computer["name"]} for computer in computers]
    print(f'{simplified_computers}')
    return jsonify(simplified_computers)


# Get specific computer details
@app.route('/api/computers/<computer_mac_address>', methods=['GET'])
def get_computer(computer_mac_address):
    computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)
    if computer:
        return jsonify(computer)
    else:
        return jsonify({"error": "מחשב לא נמצא"}), 404


# Add new computer
@app.route('/api/computers', methods=['POST'])
def add_computer():
    new_computer = request.json

    # Check if computer with this MAC_address already exists
    if any(c["mac_address"] == new_computer["mac_address"] for c in computers):
        return jsonify({"error": "מחשב עם כתובת mac זו כבר קיים"}), 400

    # Add new computer
    computers.append(new_computer)
    return jsonify(new_computer), 201


# Update computer details
@app.route('/api/computers/<computer_mac_address>', methods=['PUT'])
def update_computer(computer_mac_address):
    update_data = request.json
    computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)

    if not computer:
        return jsonify({"error": "מחשב לא נמצא"}), 404

    # Update computer fields
    if "name" in update_data:
        computer["name"] = update_data["name"]
    if "address" in update_data:
        computer["address"] = update_data["address"]

    return jsonify(computer)


# Add grade to computer
@app.route('/api/computers/<computer_mac_address>/grades', methods=['POST'])
def add_grade(computer_mac_address):
    grade_data = request.json
    computer = next((c for c in computers if c["mac_address"] == computer_mac_address), None)

    if not computer:
        return jsonify({"error": "מחשב לא נמצא"}), 404

    if "grade" not in grade_data:
        return jsonify({"error": "נתון הציון חסר"}), 400

    # Add new grade
    computer["grades"].append(grade_data["grade"])
    return jsonify(computer)


if __name__ == '__main__':
    app.run(debug=True)