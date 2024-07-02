import socket
import threading
from DB_CRUD_Functions import *
from DB_Additional_Functions import *
from DB_CRUD_Users_Functions import *
from DB_main import supabase
from Auth import *
import uuid
from rsa import *
from crypto_utils import *
import os
from rsa import rsa_encrypt

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

# -------------------------------------------- File ----------------------------------------------
def broadcast_file(file_name, file_size, file_data, id_user, channel_code, user):
    user_id_sender = get_id_by_ip(supabase,id_user[0])
    print("user_id_sender:",user_id_sender)
    users = get_session_users(supabase, channel_code)
    # Delete the current user of the list
    users = [user for user in users if user != user_id_sender]
    print("users :",users)
    for receiver_id in users:
        if receiver_id != id_user:
            receiver_info = get_connection_all(supabase, receiver_id)
            print(receiver_info)
            for connection_info in receiver_info:
                receiver_address = (connection_info['ip'], connection_info['port'])
                receiver_socket = clients.get(receiver_address)
            if receiver_socket:
                try:
                    receiver_socket.send(b'FILE')
                    receiver_socket.send(user).encode('utf-8')
                    receiver_socket.send(f"{file_name:<100}".encode('utf-8'))
                    receiver_socket.send(f"{file_size:<100}".encode('utf-8'))
                    receiver_socket.send(file_data)
                except Exception as e:
                    print(f"Error sending message to user {receiver_id}: {e}")
            else:
                print(f"User {receiver_id} socket not found.")


def receive_file(client_socket, client_address, channel_code, user):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    try:
        # Receive file metadata
        file_name = client_socket.recv(100).decode().strip()
        file_size = int(client_socket.recv(100).decode().strip())
        print(f"Receiving file: {file_name}, Size: {file_size}")

        received_file_data = b""
        while len(received_file_data) < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            received_file_data += data

        # Write received file data to a temporary file
        with open(os.path.join("temp", file_name), "wb") as file:
            file.write(received_file_data)

        print(f"File {file_name} transfer complete.")

        # Broadcast the received file to all clients except the source
        broadcast_file(file_name, file_size, received_file_data, client_address, channel_code, user)

    except Exception as e:
        print(f"Error receiving file from {client_address}: {e}")

# -------------------------------------------- File ----------------------------------------------

def client_handler(id_user, client_socket, client_address, channel_code, lock, aes_key, public_key):
    id_user_uuid = uuid.UUID(id_user)
    clients[client_address] = client_socket
    try:
        encrypted_aes_key = rsa_encrypt(aes_key, public_key)
        client_socket.recv(1024) # Wait for the client to be ready to receive the encrypted AES key
        client_socket.send(encrypted_aes_key)
        while not stop_event.is_set():
            message_type = client_socket.recv(1024)
            user = client_socket.recv(1024).decode('utf-8')
            if message_type:
                if message_type == b"DISCONNECT":
                    print(f"Client {client_address} in channel {channel_code} is disconnecting.")
                    break
                elif message_type == b"FILE":
                    receive_file(client_socket, client_address, channel_code, user)
                elif message_type == b"TEXT":
                    message = client_socket.recv(1024)
                    with lock:
                        users = get_session_users(supabase, channel_code)
                        for receiver_id in users:
                            if receiver_id != id_user:
                                receiver_info = get_connection_all(supabase, receiver_id)
                                print(receiver_info)
                                for connection_info in receiver_info:
                                    receiver_address = (connection_info['ip'], connection_info['port'])
                                    receiver_socket = clients.get(receiver_address)
                                if receiver_socket:
                                    try:
                                        receiver_socket.send(b'TEXT')
                                        receiver_socket.send(user).encode('utf-8')
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


def join_channel(client_socket,client_address, channel_code, id_user, lock,aes_key, public_key):
    try:
        session_exist = is_session_in_database(supabase, channel_code)
        if session_exist :
            ip = client_address[0]
            port = client_address[1]
            create_new_connection(supabase, id_user, channel_code, ip, port)
            add_next_user_in_session(supabase, channel_code, id_user)
        else:
            print(f"Channel {channel_code} does not exist.")

        # Start client handler thread for this client and channel
        threading.Thread(target=client_handler,
                         args=(
                         id_user, client_socket, client_socket.getpeername(), channel_code, lock,aes_key, public_key)).start()
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
    aes_key = generate_aes_key()

    server_socket.listen(5)
    print("Server listening on", server_socket.getsockname(), "...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted a new connection from {client_address}")

            # Receive the channel code from the client
            channel_code = client_socket.recv(1024).decode('utf-8')
            print("Received channel code:", channel_code)
            client_socket.send(b"Channel code received.")

            public_key = client_socket.recv(1024)
            client_socket.send(b"Public key received.")

            id_user = client_socket.recv(1024).decode('utf-8')
            print("Received user ID:", id_user)
            client_socket.send(b"User ID received.")

            join_channel(client_socket, client_address, channel_code, id_user, lock, aes_key, public_key)

    except Exception as e:
        print("Server error:", e)
    finally:
        log_out_user(supabase)
        delete_server(supabase, ip)
        server_socket.close()

if __name__ == "__main__":
    start_server()
