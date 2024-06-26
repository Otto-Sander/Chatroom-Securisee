import socket
import threading
from DB_CRUD_Functions import *
from DB_main import supabase
from crypto_utils import *
from rsa import *

lock = threading.Lock()
server_socket = None
channel_connections = {}  # Dictionnaire pour stocker les connexions par canal

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

def get_server_port():
    global server_socket
    if server_socket:
        try:
            ip, server_port = server_socket.getsockname()
            return server_port
        except socket.error as e:
            print(f"Erreur lors de la récupération du port du serveur : {e}")
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


def client_handler(client_socket, client_address, channel_code, connections, lock, public_key):
    try:
        aes_key = generate_aes_key()
        encrypted_aes_key = rsa_encrypt(aes_key, public_key)
        client_socket.send(base64.b64encode(encrypted_aes_key))

        while True:
            message = client_socket.recv(1024).decode('ascii')
            if message:
                with lock:
                    for connection in connections[channel_code]:
                        if connection[0] != client_socket:
                            connection[0].send(message.encode('ascii'))
    except Exception as e:
        print(f"Error in client handler: {e}")
    finally:
        with lock:
            connections[channel_code].remove((client_socket, public_key))
        client_socket.close()


def join_channel(client_socket, channel_code, connections, lock, public_key):
    with lock:
        if channel_code not in connections:
            connections[channel_code] = []
        connections[channel_code].append((client_socket, public_key))

    threading.Thread(target=client_handler, args=(client_socket, client_socket.getpeername(), channel_code, connections, lock, public_key)).start()

def start_server():
    ip = get_private_ip()
    port = find_free_port()

    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    add_server(supabase, ip, port)
    server_socket.listen(5)
    print("Server listening on", server_socket.getsockname(), "...")

    connections = {}

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            public_key = client_socket.recv(4096).decode('utf-8')  # Assuming public key sent right after connection
            channel_code = client_socket.recv(1024).decode('utf-8')
            print(f"Accepted new connection from {client_address} in channel {channel_code}")
            join_channel(client_socket, channel_code, connections, lock, public_key)
    except Exception as e:
        print("Server error:", e)
    finally:
        delete_server(supabase, ip)
        server_socket.close()

if __name__ == "__main__":
    start_server()
