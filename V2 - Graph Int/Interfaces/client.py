import socket
import threading
import json
import os

def enter_server(ip,port,canal):
    os.system('cls||clear')
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        print(f"Connected to server at {ip}:{port}")

        # Choose a channel
        # channel = input("Enter the channel you want to join: ")
        # client.send(channel.encode('ascii'))

        def receive():
            while True:
                try:
                    message = client.recv(1024).decode('ascii')
                    if message:
                        print(message)
                except Exception as e:
                    print("Error receiving messages:", e)
                    break

        def write():
            while True:
                try:
                    message = input("")
                    client.send(f'{message}'.encode('ascii'))
                except Exception as e:
                    print("Error sending messages:", e)
                    break

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()

    except Exception as e:
        print(f"Error connecting to server: {e}")
