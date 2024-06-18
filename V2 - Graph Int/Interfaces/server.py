import socket
import threading

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

def start_server():
    ip = get_private_ip()
    port = find_free_port()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))

    server_socket.listen(5)
    print("Server listening on", server_socket.getsockname(), "...")

    connections = []  # Initialize a list for all connections
    lock = threading.Lock()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted a new connection from {client_address}")

            # Uncomment the following lines for channel functionality
            # client_socket.send(b"Enter channel:")
            # channel = client_socket.recv(1024).decode('ascii')

            with lock:
                connections.append(client_socket)

            threading.Thread(target=client_handler, args=(client_socket, client_address, connections, lock)).start()
    except Exception as e:
        print("Server error:", e)
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
