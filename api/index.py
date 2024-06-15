import os
import json
import base64
import hashlib
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

if not os.path.exists('tmp'):
    os.makedirs('tmp')

encryption_key = 'encrypt nigga nigger jew faggot slave monkey faggot tranny dude this is the actual encryption alg im not lying onb'

def encrypt_data(data):
    encrypted_chars = []
    for char in data:
        encrypted_char = chr(ord(char) + len(encryption_key))
        encrypted_chars.append(encrypted_char)
    encrypted_data = ''.join(encrypted_chars)
    return base64.urlsafe_b64encode(encrypted_data.encode()).decode()

def decrypt_data(encrypted_data):
    decrypted_chars = []
    decrypted_data = base64.urlsafe_b64decode(encrypted_data.encode()).decode()
    for char in decrypted_data:
        decrypted_char = chr(ord(char) - len(encryption_key))
        decrypted_chars.append(decrypted_char)
    return ''.join(decrypted_chars)

def save_data(data):
    encrypted_data = {}
    for key, value in data.items():
        encrypted_data[key] = encrypt_data(value)
    filepath = os.path.join('tmp', 'data.json')
    with open(filepath, 'w') as file:
        json.dump(encrypted_data, file)

def load_data():
    filepath = os.path.join('tmp', 'data.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            encrypted_data = json.load(file)
            data = {}
            for key, value in encrypted_data.items():
                data[key] = decrypt_data(value)
            return data
    return {}

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    code = data.get('code')
    anonymous = data.get('anonymous', False)

    if not code:
        return jsonify({'error': 'Code is required'}), 400

    ip_address = request.remote_addr
    username = ip_address if not anonymous else 'Anonymous'

    saved_data = load_data()

    if code in saved_data.values():
        return jsonify({'error': 'Code already exists'}), 400

    saved_data[username] = code
    save_data(saved_data)

    return jsonify({'message': 'Code submitted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)