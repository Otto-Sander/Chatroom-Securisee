import socket
import threading
from DB_CRUD_Functions import *
from DB_Additional_Functions import *
from DB_CRUD_Users_Functions import *
from DB_main import supabase
from Auth import *
import uuid

server_socket = None
stop_event = threading.Event()

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

def client_handler(id_user, client_socket, client_address, channel_code, lock):
    id_user_uuid = uuid.UUID(id_user)
    try:
        while not stop_event.is_set():
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
                            receiver_id_uuid = uuid.UUID(receiver_id)
                            print(f"Sending message to user {receiver_id}.")
                            ip = get_connection_ip(supabase, receiver_id_uuid)
                            port = get_connection_port(supabase, receiver_id_uuid)
                            print (f"IP: {ip}, Port: {port}")
                            send_message_to_user(ip, port, message)
            else:
                break
    except Exception as e:
        print(f"Client handler error in channel {channel_code}: {e}")
    finally:
        with lock:
            delete_connection(supabase, id_user_uuid)
            delete_user_in_session(supabase, channel_code, id_user_uuid)
            remaining_users = get_session_users(supabase, channel_code)
            if not remaining_users:
                delete_session(supabase, channel_code)
        client_socket.close()

def send_message_to_user(ip, port, message):
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the user's IP and port
        sock.connect((ip, port))
        # Send the message
        if isinstance(message, str):
            sock.send(message.encode('utf-8'))  # Encode the message to bytes if it's a string
        else:
            sock.send(message)  # Directly send if it's already bytes
        # Close the socket
        sock.close()
        print(f"Message sent to {ip}:{port}: {message}")

    except Exception as e:
        print(f"Error sending message to {ip}:{port}: {e}")


def join_channel(client_socket,client_address, channel_code, id_user, lock):
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
                         id_user, client_socket, client_socket.getpeername(), channel_code, lock)).start()
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

if __name__ == "__main__":
    start_server()
