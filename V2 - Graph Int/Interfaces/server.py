import socket
import threading
from DB_CRUD_Functions import *
from DB_main import supabase

lock = threading.Lock()
server_socket = None

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

def client_handler(client_socket, client_address, connections, lock):
    try:
        # Handle client messages within a specific channel
        while True:
            message = client_socket.recv(1024)
            if message:
                print(f"Message from {client_address}: {message}")
                with lock:
                    for connection in connections:
                        if connection != client_socket:
                            connection.send(message)
            else:
                break
    except Exception as e:
        print("Client handler error:", e)
    finally:
        with lock:
            connections.remove(client_socket)
        client_socket.close()

def join_channel(client_socket, channel_code, connections, lock):
    try:
        session = get_all_codes(supabase)
        if session:
            ip, port = get_last_server(supabase)
            client_socket.send(b"Channel joined successfully.")
            client_socket.send(f"IP privée du serveur: {ip}, port {port}.".encode('utf-8'))

            # Start client handler thread for this client and channel
            threading.Thread(target=client_handler,
                             args=(client_socket, client_socket.getpeername(), connections, lock)).start()
        else:
            client_socket.send(b"Channel does not exist in the database.")
            print(f"Channel {channel_code} does not exist in the database.")
            client_socket.close()
    except Exception as e:
        print("Error joining channel:", e)
        client_socket.close()


def start_server():
    ip = get_private_ip()
    port = find_free_port()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    add_server(supabase, ip, port)

    server_socket.listen(5)
    print("Server listening on", server_socket.getsockname(), "...")

    connections = []  # Initialize a list for all connections
    lock = threading.Lock()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted a new connection from {client_address}")

            # Receive the channel code from the client
            channel = client_socket.recv(1024).decode('utf-8')
            print(f"Client connected to channel: {channel}")

            # Join the channel
            join_channel(client_socket, channel, connections, lock)

            # Optionally, you can uncomment these lines if you want to prompt the client to enter a channel
            # client_socket.send(b"Enter channel:")
            # channel = client_socket.recv(1024).decode('utf-8')

            with lock:
                connections.append(client_socket)

            # Start a thread to handle the client's messages
            threading.Thread(target=client_handler, args=(client_socket, client_address, connections, lock)).start()

    except Exception as e:
        print("Server error:", e)
    finally:
        delete_server(supabase, ip)
        server_socket.close()

if __name__ == "__main__":
    start_server()
