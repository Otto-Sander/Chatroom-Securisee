import socket
import threading
from rsa import *
from crypto_utils import *
import os



def enter_server(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    private_key, public_key = generate_rsa_keys()

    # Send public key to server
    client_socket.send(public_key)

    # Receive AES key encrypted with RSA public key
    encrypted_aes_key = client_socket.recv(1024)
    aes_key = rsa_decrypt(encrypted_aes_key, private_key)

    def receive():
        while True:
            try:
                message = client_socket.recv(1024).decode('ascii')
                print("Encrypted message:", message)
                decrypted_message = aes_decrypt(message, aes_key)
                print("Decrypted message:", decrypted_message)
            except Exception as e:
                print("Error receiving messages:", e)
                break

    def send():
        while True:
            message = input("Enter your message: ")
            encrypted_message = aes_encrypt(message, aes_key)
            client_socket.send(encrypted_message.encode('ascii'))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()

if __name__ == "__main__":
    enter_server('127.0.0.1', 12345)
