import socket
import threading
from DB_CRUD_Functions import *
from DB_Additional_Functions import *
from DB_CRUD_Users_Functions import *
from DB_main import supabase
from Auth import *
import uuid
import os
from rsa import rsa_encrypt
from rsa import generate_rsa_keys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from crypto_utils import *

server_socket = None
stop_event = threading.Event()
clients = {}

def get_private_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Erreur lors de la récupération de l'adresse IP : {e}")
        return None

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def generate_aes_key():
    return AES.get_random_bytes(32)  # AES key generation (256 bits)

def client_handler(id_user, client_socket, client_address, channel_code, lock,public_key):
    id_user_uuid = uuid.UUID(id_user)
    clients[client_address] = client_socket
    try:
        while not stop_event.is_set():
            aes_key = generate_aes_key()
            encrypted_aes_key = rsa_encrypt(aes_key, public_key)
            client_socket.send(base64.b64encode(encrypted_aes_key))


            message = client_socket.recv(1024)
            if message:
                if message == b"DISCONNECT":
                    print(f"Client {client_address} in channel {channel_code} is disconnecting.")
                    break
                print(f"Message from {client_address} in channel {channel_code}: {message}")
                with lock:
                    users = get_session_users(supabase, channel_code)
                    print(users)
                    for receiver_id in users:
                        if receiver_id != id_user:
                            receiver_info = get_connection_all(supabase, receiver_id)
                            print(receiver_info)
                            for connection_info in receiver_info:
                                receiver_address = (connection_info['ip'], connection_info['port'])
                                receiver_socket = clients.get(receiver_address)
                            if receiver_socket:
                                try:
                                    receiver_socket.send(message)
                                    print(f"Message sent to user {receiver_id}")
                                except Exception as e:
                                    print(f"Error sending message to user {receiver_id}: {e}")
                            else:
                                print(f"User {receiver_id} socket not found.")
            else:
                break
    except Exception as e:
        print(f"Client handler error in channel {channel_code}: {e}")
    finally:
        with lock:
            delete_connection(supabase, id_user_uuid)
            delete_user_in_session(supabase, channel_code, id_user)
            remaining_users = get_session_users(supabase, channel_code)
            if not remaining_users:
                delete_session(supabase, channel_code)
        client_socket.close()


def join_channel(client_socket,client_address, channel_code, id_user, lock, public_key):
    try:
        session_exist = is_session_in_database(supabase, channel_code)
        if session_exist :
            ip = client_address[0]
            port = client_address[1]
            create_new_connection(supabase, id_user, channel_code, ip, port)
            add_next_user_in_session(supabase, channel_code, id_user)
        else:
            print(f"Channel {channel_code} does not exist.")

        client_socket.send(b"Channel joined successfully.")

        # Start client handler thread for this client and channel
        threading.Thread(target=client_handler,
                         args=(
                         id_user, client_socket, client_socket.getpeername(), channel_code, lock,public_key)).start()
    except Exception as e:
        print(f"Error joining channel {channel_code}: {e}")
        client_socket.close()

def start_server():
    log_in_user(supabase, "nathan.simoes93@gmail.com","rootroot")
    print(get_current_connected_user_id(supabase))
    ip = get_private_ip()
    port = find_free_port()

    lock = threading.Lock()

    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    create_new_server(supabase, ip, port)

    server_socket.listen(5)
    print("Server listening on", server_socket.getsockname(), "...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted a new connection from {client_address}")

            
            rsa_keys = generate_rsa_keys()

            # Receive the channel code from the client
            channel_code = client_socket.recv(1024).decode('utf-8')
            print("Received channel code:", channel_code)
            client_socket.send(b"Channel code received.")

            id_user = client_socket.recv(1024).decode('utf-8')
            print("Received user ID:", id_user)
            client_socket.send(b"User ID received.")
            print(f"User ID: {id_user}")
            join_channel(client_socket, client_address, channel_code, id_user, lock)

    except Exception as e:
        print("Server error:", e)
    finally:
        log_out_user(supabase)
        delete_server(supabase, ip)
        server_socket.close()
# ------------------------------------------------------------------
    def send_file(self, file_name, file_size, file_data):
        try:
            self.socket.sendall("FILE".encode())
            self.socket.sendall(f"{file_name:<100}".encode('utf-8'))
            self.socket.sendall(f"{file_size:<100}".encode('utf-8'))
            self.socket.sendall(file_data)
            print(f"File {file_name} sent to {self.address}")
        except Exception as e:
            print("Send file error:", e)


    def receive_file(self):
        if not os.path.exists("temp"):
            os.makedirs("temp")

        file_name = self.socket.recv(100).decode().strip()
        file_size = int(self.socket.recv(100).decode().strip())
        print(f"Receiving file: {file_name}, Size: {file_size}")

        encoded_file_data = b""
        while len(encoded_file_data) < file_size:
            data = self.socket.recv(1024)
            if not data:
                break
            encoded_file_data += data

        # Déchiffrement du fichier
        decrypted_file_data = aes_decrypt(base64.b64decode(encoded_file_data).decode('utf-8'), self.server.aes_key)
        decoded_file_data = base64.b64decode(decrypted_file_data.encode('utf-8'))

        with open(os.path.join("temp", file_name), "wb") as file:
            file.write(decoded_file_data)

        print(f"File {file_name} transfer complete.")

        # Broadcast the file to other clients
        self.server.broadcast_file(file_name, file_size, encoded_file_data, self.address)

    def broadcast_file(self, file_name, file_size, file_data, source):
        with self.lock:
            for connection in self.connections:
                if connection.address != source:
                    connection.send_file(file_name, file_size, file_data)

if __name__ == "__main__":
    start_server()
