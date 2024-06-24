import socket
import threading
from DB_CRUD_Functions import *
from DB_main import supabase

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

def client_handler(client_socket, client_address, channel_code, connections, lock):
    try:
        # Handle client messages within a specific channel
        while True:
            message = client_socket.recv(1024)
            if message:
                print(f"Message from {client_address} in channel {channel_code}: {message}")
                with lock:
                    for connection in connections[channel_code]:
                        if connection != client_socket:
                            connection.send(message)
            else:
                break
    except Exception as e:
        print(f"Client handler error in channel {channel_code}: {e}")
    finally:
        with lock:
            connections[channel_code].remove(client_socket)
        client_socket.close()

def join_channel(client_socket, channel_code, connections, lock):
    try:
        if channel_code in connections:
            connections[channel_code].append(client_socket)
        else:
            connections[channel_code] = [client_socket]

        client_socket.send(b"Channel joined successfully.")

        # Start client handler thread for this client and channel
        threading.Thread(target=client_handler,
                         args=(client_socket, client_socket.getpeername(), channel_code, connections, lock)).start()

    except Exception as e:
        print(f"Error joining channel {channel_code}: {e}")
        client_socket.close()

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

    connections = {}  # Initialize a dictionary for all connections by channel
    lock = threading.Lock()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted a new connection from {client_address}")

            # Receive the channel code from the client
            channel_code = client_socket.recv(1024).decode('utf-8')
            print(f"Client connected to channel: {channel_code}")

            # Join the channel
            join_channel(client_socket, channel_code, connections, lock)

    except Exception as e:
        print("Server error:", e)
    finally:
        delete_server(supabase, ip)
        server_socket.close()

if __name__ == "__main__":
    start_server()
