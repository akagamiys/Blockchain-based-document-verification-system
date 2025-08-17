from flask import Flask, render_template, request, jsonify
import os
from generate_fingerprint import generate_blake2b_fingerprint
from encryption import encrypt_file
from decryption import decrypt_file
import requests
import subprocess
import re


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['file']
    password = request.form['password']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        encrypted_file = os.path.join(UPLOAD_FOLDER, 'encrypted_' + file.filename)
        encrypt_file(filepath, encrypted_file, password)
        fingerprint = generate_blake2b_fingerprint(encrypted_file)
        objid,pacid = store_fingerprint_on_sui(fingerprint)
        return render_template('index.html', message="File encrypted successfully and fingerprint stored on SUI blockchain",fingerprint=fingerprint,
            object_id=objid,
            package_id=pacid)
    return render_template('index.html', error="No file uploaded")

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['file']
    password = request.form['password']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        decrypted_file = os.path.join(UPLOAD_FOLDER, 'decrypted_' + file.filename)
        decrypt_file(filepath, decrypted_file, password)
        return render_template('index.html', message="File decrypted successfully", decrypted_file=decrypted_file)
    return render_template('index.html', error="No file uploaded")

@app.route('/check_fingerprint', methods=['POST'])
def check_fingerprint():
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        fingerprint = generate_blake2b_fingerprint(filepath)
        is_valid = check_fingerprint_on_sui(fingerprint)
        if is_valid:
            return render_template('index.html', message="Fingerprint verified on SUI blockchain", fingerprint=fingerprint)
        else:
            return render_template('index.html', error="Fingerprint not found on SUI blockchain")
    return render_template('index.html', error="No file uploaded")

def store_fingerprint_on_sui(fingerprint):
    command = "sui client publish --gas-budget 100000000 --skip-fetch-latest-git-deps"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    if result.returncode == 0:
        print("Contract published successfully.")
    else:
        print("Failed to publish contract.")

    object_ids = re.findall(r"ObjectID:\s(0x[a-fA-F0-9]+)", result.stdout)
    object_id = object_ids[0]
    # Extract Package ID
    package_ids = re.findall(r"PackageID:\s(0x[a-fA-F0-9]+)", result.stdout)
    package_id = package_ids[0]
    print("Object IDs:", object_id)
    print("Package IDs:", package_id)
    print(f"Storing fingerprint on SUI: {fingerprint}")
    return object_id , package_id


def check_fingerprint_on_sui(fingerprint,package_id):
    module_name = "document_registry"
    function_name = "get_fingerprint"
    
    command = f"sui client call --package {package_id} --module {module_name} --function {function_name} --gas-budget 50000000"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")

    if result.returncode != 0:
        print("Error retrieving fingerprint from SUI blockchain")
        return False

    stored_fingerprints = re.findall(r"Fingerprint:\s(0x[a-fA-F0-9]+)", result.stdout)

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    if fingerprint in stored_fingerprints:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)