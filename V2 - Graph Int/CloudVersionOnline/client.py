import socket


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("7.tcp.eu.ngrok.io",17934))

print(client.recv(1024).decode())
client.send("Hey server".encode())