# Blockchain-Based Encrypted Document Verification

A **Flask-based web application** for securely encrypting, decrypting, and verifying documents using the **Sui blockchain**.  
Instead of storing entire files, the system generates a **Blake2b fingerprint (hash)** of the file and stores it on-chain, ensuring **immutability, authenticity, and tamper-proof verification**.

---

## 🚀 Features
- 🔐 **AES Encryption & Decryption** with a user-provided password  
- 🧾 **Blake2b Fingerprint Generation** for unique file identifiers  
- ⛓ **Blockchain Integration** with Sui blockchain for fingerprint storage & verification  
- ✅ **Integrity Checking** – verify if a document’s fingerprint exists on-chain  
- 🌐 **Flask Web UI** for file uploads and interactions  

---

## 📜 Usage
🔐 Encrypt a File
 - Upload a file and provide a password
 - The file gets encrypted and its fingerprint is stored on the blockchain

🔓 Decrypt a File
 - Upload the encrypted file with the correct password
 - The decrypted file is provided for download

✅ Verify Fingerprint
 - Upload a file
 - The system generates its fingerprint and checks the Sui blockchain for verification

---

## 🛡 Security Notes
 - Passwords are not stored anywhere
 - Only fingerprints (hashes) are stored on the blockchain
 - Uploaded files are temporary and ignored in Git

---

## 📌 Prerequisites
 - Install Sui CLI
 - Deploy the Move contract once to obtain your SUI_PACKAGE_ID

--- 
