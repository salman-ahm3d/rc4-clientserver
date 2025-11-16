# RC4 Encrypted Chat with Integrity Verification

A Python-based client-server chat application developed for a Wireless and Mobile Security project. This tool implements the RC4 stream cipher from scratch and utilizes a custom checksum mechanism to ensure message confidentiality and integrity over TCP sockets.

## Features
* **RC4 Encryption:** Custom implementation of the RC4 Key Scheduling Algorithm (KSA) and Pseudo-Random Generation Algorithm (PRGA).
* **Integrity Check:** Implements a custom 32-bit checksum calculation appended to the plaintext to detect data tampering.
* **Full-Duplex Communication:** Uses Python `threading` to allow simultaneous sending and receiving of messages.
* **Pre-Shared Key (PSK):** authentication using a hardcoded shared key.

## Project Structure
* `rc4.py`: Contains the RC4 encryption/decryption logic and custom checksum algorithm.
* `server.py`: Multi-threaded server that binds to `0.0.0.0:9999`.
* `client.py`: Multi-threaded client that connects to `127.0.0.1:9999`.

## Usage

### Prerequisites
* Python 3.x

### 1. Start the Server
Run the server script first. It will listen for incoming connections on port 9999.
```bash
python server.py
```

### 2. Start the Client
Open a new terminal and run the client script.
```bash
python client.py
```

### 3. Exchange Messages
Type messages in either terminal. Data is encrypted locally, transmitted, and decrypted/verified on the receiving end.

## Configuration
To modify connection settings or the encryption key, edit the following variables in server.py and client.py:
```
Key: PSK = "sharedkey"
Host/Port: 127.0.0.1 / 9999
```

## Disclaimer

This project is for educational purposes to demonstrate stream cipher implementation and manual integrity verification. It is not intended for production security environments.
