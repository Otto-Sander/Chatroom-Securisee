import socket
import threading
from rsa import *
from crypto_utils import *
import os
import time



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


########################################## NEW FUNCTIONS #################################################

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

                client_socket.sendall("FILE".encode())
                client_socket.sendall(f"{os.path.basename(file_path):<100}".encode('utf-8'))
                client_socket.sendall(f"{len(encoded_file_data):<100}".encode('utf-8'))

                client_socket.sendall(encoded_file_data.encode('utf-8'))

            print("Transfert de fichier terminé.")
        except Exception as e:
            print("Erreur lors de l'envoi du fichier:", e)

    def receive_file():
        if not os.path.exists("temp"):
            os.makedirs("temp")

        file_name = client_socket.recv(100).decode().strip()
        file_size = int(client_socket.recv(100).decode().strip())

        encoded_file_data = b""
        while len(encoded_file_data) < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            encoded_file_data += data

        # Déchiffrement du fichier
        decrypted_file_data = aes_decrypt(base64.b64decode(encoded_file_data).decode('utf-8'), aes_key)
        decoded_file_data = base64.b64decode(decrypted_file_data.encode('utf-8'))

        with open(os.path.join("temp", file_name), "wb") as file:
            file.write(decoded_file_data)

        print("Transfert de fichier terminé.")
##############################################################################################################
if __name__ == "__main__":
    enter_server('127.0.0.1', 12345)
