import socket
import threading
import os
import uuid

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


def send_file(client_socket, file_name, file_size, file_data):
    try:
        client_socket.sendall("FILE".encode())
        client_socket.sendall(f"{file_name:<100}".encode('utf-8'))
        client_socket.sendall(f"{file_size:<100}".encode('utf-8'))
        client_socket.sendall(file_data)
        print(f"File {file_name} sent")
    except Exception as e:
        print("Send file error:", e)


def broadcast_file(file_name, file_size, file_data, source):
    for client_addr, client_socket in clients.items():
        if client_addr != source:
            send_file(client_socket, file_name, file_size, file_data)


def receive_file(client_socket):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    file_name = client_socket.recv(100).decode().strip()
    file_size = int(client_socket.recv(100).decode().strip())
    print(f"Receiving file: {file_name}, Size: {file_size}")

    received_file_data = b""
    while len(received_file_data) < file_size:
        data = client_socket.recv(1024)
        if not data:
            break
        received_file_data += data

    with open(os.path.join("temp", file_name), "wb") as file:
        file.write(received_file_data)

    print(f"File {file_name} transfer complete.")
    return file_name, file_size, received_file_data


def client_handler(client_socket, client_address):
    clients[client_address] = client_socket
    try:
        while not stop_event.is_set():
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message == "DISCONNECT":
                    print(f"Client {client_address} is disconnecting.")
                    break
                elif message == "FILE":
                    file_name, file_size, file_data = receive_file(client_socket)
                    broadcast_file(file_name, file_size, file_data, client_address)
                else:
                    print(f"Message from {client_address}: {message}")
                    for client_addr, sock in clients.items():
                        if client_addr != client_address:
                            sock.send(message.encode('utf-8'))
            else:
                break
    except Exception as e:
        print(f"Client handler error: {e}")
    finally:
        client_socket.close()
        del clients[client_address]


def start_server():
    ip = get_private_ip()
    port = find_free_port()

    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))

    server_socket.listen(5)
    print("Server listening on", server_socket.getsockname(), "...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted a new connection from {client_address}")

            threading.Thread(target=client_handler, args=(client_socket, client_address)).start()
    except Exception as e:
        print("Server error:", e)
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
