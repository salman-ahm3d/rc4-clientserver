import socket
import threading
from rc4 import encrypt_with_checksum, decrypt_with_checksum  # Import updated RC4 functions

# Pre-shared key
PSK = "sharedkey"

# Handle client connection
def handle_client(client_socket):
    try:
        while True:
            # Receive and decrypt the message
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            try:
                decrypted_message = decrypt_with_checksum(PSK, encrypted_message)
                print(f"Client: {decrypted_message}")
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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server started, waiting for connections...")

    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=handle_client, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        print(f"Server error: {e}")
