import socket
import threading
import json
import os
from rsa import generate_rsa_keys
from rsa import rsa_decrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from crypto_utils import *
import time

def enter_server(ip,port,canal):
    os.system('cls||clear')
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        private_key, public_key = generate_rsa_keys()

        # Send public key to server
        client.send(public_key)

        print(f"Connected to server at {ip}:{port}")

        # Choose a channel
        # channel = input("Enter the channel you want to join: ")
        # client.send(channel.encode('ascii'))

         # Receive AES key encrypted with RSA public key
        encrypted_aes_key = client.recv(1024)
        aes_key = rsa_decrypt(encrypted_aes_key, private_key)

        def receive():
            while True:
                try:
                    message = client.recv(1024).decode('ascii')
                    if message:
                        print(message)
                        print("Encrypted message:", message)
                        decrypted_message = aes_decrypt(message, aes_key)
                        print("Decrypted message:", decrypted_message)
                except Exception as e:
                    print("Error receiving messages:", e)
                    break

        def write():
            while True:
                try:
                    message = input("")
                    encrypted_message = aes_encrypt(message, aes_key)
                    client.send(encrypted_message.encode('ascii'))
                except Exception as e:
                    print("Error sending messages:", e)
                    break

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()

        def send_file():
            try:
                file_path = input("Entrez le chemin complet du fichier à envoyer: ")
                if not os.path.isfile(file_path):
                    print("Le fichier n'existe pas. Veuillez vérifier le chemin.")
                    return

                file_size = os.path.getsize(file_path)

                with open(file_path, "rb") as file:
                    # Starting the time capture.
                    start_time = time.time()
                    file_data = file.read()

                    # Chiffrement du fichier
                    encrypted_file_data = aes_encrypt(base64.b64encode(file_data).decode('utf-8'), aes_key)
                    encoded_file_data = base64.b64encode(encrypted_file_data.encode('utf-8')).decode('utf-8')

                    client.sendall("FILE".encode())
                    client.sendall(f"{os.path.basename(file_path):<100}".encode('utf-8'))
                    client.sendall(f"{len(encoded_file_data):<100}".encode('utf-8'))

                    client.sendall(encoded_file_data.encode('utf-8'))

                print("Transfert de fichier terminé.")
            except Exception as e:
                print("Erreur lors de l'envoi du fichier:", e)

        def receive_file():
            if not os.path.exists("temp"):
                os.makedirs("temp")

            file_name = client.recv(100).decode().strip()
            file_size = int(client.recv(100).decode().strip())

            encoded_file_data = b""
            while len(encoded_file_data) < file_size:
                data = client.recv(1024)
                if not data:
                    break
                encoded_file_data += data

            # Déchiffrement du fichier
            decrypted_file_data = aes_decrypt(base64.b64decode(encoded_file_data).decode('utf-8'), aes_key)
            decoded_file_data = base64.b64decode(decrypted_file_data.encode('utf-8'))

            with open(os.path.join("temp", file_name), "wb") as file:
                file.write(decoded_file_data)

            print("Transfert de fichier terminé.")

    except Exception as e:
        print(f"Error connecting to server: {e}")
