import socket
import threading
from rc4 import encrypt_with_checksum, decrypt_with_checksum  # Import updated RC4 functions

# Pre-shared key
PSK = "sharedkey"

def receive_messages(client_socket):
    try:
        while True:
            # Receive and decrypt the message
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            try:
                decrypted_message = decrypt_with_checksum(PSK, encrypted_message)
                print(f"Server: {decrypted_message}")
            except ValueError as e:
                print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def send_messages(client_socket):
    try:
        while True:
            # Get user input and encrypt the message
            message = input("")
            encrypted_message = encrypt_with_checksum(PSK, message)
            client_socket.sendall(encrypted_message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    print("Connected to the server.")

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    send_thread = threading.Thread(target=send_messages, args=(client,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    try:
        start_client()
    except Exception as e:
        print(f"Client error: {e}")
