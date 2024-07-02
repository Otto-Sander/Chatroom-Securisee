import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import threading
import socket
from DB_main import supabase
from DB_CRUD_Functions import *
from Auth import *
from rsa import *
from crypto_utils import *
import os
from crypto_utils import aes_decrypt
from rsa import generate_rsa_keys
from rsa import rsa_decrypt
from DB_CRUD_Users_Functions import *

client_socket = None

def open_chatroom(previous_win, width_win, height_win, code):

    # Récupère le username actuel
    username = get_username(supabase,get_current_connected_user_email(supabase))

    def on_close():
        try:
            # Send a "disconnect" message to the server
            if client_socket:
                client_socket.sendall(b"DISCONNECT")
        except Exception as e:
            print(f"Error sending disconnect message: {e}")

        # Close the socket
        if client_socket:
            client_socket.close()

        root.destroy()
        previous_win.deiconify()
        previous_win.geometry(f"{width_win}x{height_win}")
        previous_win.state('normal')
        previous_win.attributes("-alpha", 1.0)

    def display_message(chat_box, user, message):
        current_time = datetime.datetime.now()
        current_time_string = current_time.strftime("%H:%M")

        if user == username:
            bg_color = "#222222"
            text_color = "#FFFFFF"
        else:
            bg_color = "#333333"
            text_color = "#FFFFFF"

        chat_box.configure(state=tk.NORMAL)
        chat_box.tag_config("time", foreground="#888888")
        chat_box.tag_config("user", background=bg_color, foreground=text_color)
        chat_box.insert(tk.END, f"({current_time_string}) ", "time")
        chat_box.insert(tk.END, f"{user}: {message}\n", "user")
        chat_box.configure(state=tk.DISABLED)
        chat_box.see(tk.END)

    previous_win.withdraw()

    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    window_width = 600
    window_height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.title("Data Room Virtuelle")

    chat_frame = ctk.CTkFrame(root)
    chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    chat_box = ctk.CTkTextbox(chat_frame, state=tk.DISABLED, wrap=tk.WORD)
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    input_frame = tk.Frame(root)
    input_frame.pack(padx=10, pady=5, fill=tk.X)

    message_entry = ctk.CTkEntry(input_frame, placeholder_text="Écrire un message...")
    message_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)

    message_entry.bind("<Return>", lambda event: send_message(chat_box, message_entry, client_socket, aes_key))

    try:
        ip, port = get_last_server(supabase)
        user_id = get_current_connected_user_id(supabase)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        private_key, public_key = generate_rsa_keys()
        client_socket.connect((ip, port))
        client_socket.send(code.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

        client_socket.send(public_key)
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

        user_id_str = str(user_id)
        client_socket.send(user_id_str.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

        client_socket.send(b"OK")
        encrypted_aes_key = client_socket.recv(1024)

        aes_key = rsa_decrypt(encrypted_aes_key, private_key)

        display_message(chat_box, "ChatRoom", f"Welcome to the chat room! Share this code to invite others: {code}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de se connecter au serveur : {e}")
        on_close()
        return


    def send_message(chat_box, message_entry, client, aes_key):
        client.send(b"TEXT")
        client.send(username)
        message = message_entry.get()
        if message:
            try:
                encrypted_message = aes_encrypt(message, aes_key)
                client.send(encrypted_message.encode('utf-8'))
                print(encrypted_message)
                display_message(chat_box, username, message)
                message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'envoyer le message : {e}")
        else:
            messagebox.showwarning("Attention", "Veuillez saisir un message.")

    def receive_messages(aes_key):
        while True:
            try:
                message_type = client_socket.recv(4)
                user = client_socket.recv(100).decode('utf-8')
                if message_type == b"FILE":
                    file_name = client_socket.recv(100).decode('utf-8').strip()
                    file_size = int(client_socket.recv(100).decode('utf-8').strip())
                    file_data = b""

                    while len(file_data) < file_size:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        file_data += data

                    # Message box
                    response = messagebox.askyesno("Received file !", f"Do you want to save '{file_name}' from {user} ?")

                    if response:
                        # Ask user to select save location
                        file_path = filedialog.asksaveasfilename(initialfile=file_name,
                                                                 filetypes=[("All Files", "*.*")])
                        if file_path:
                            with open(file_path, "wb") as file:
                                file.write(file_data)
                            display_message(chat_box, "Other", f"File received and saved: {file_name}")
                        else:
                            display_message(chat_box, "Other", f"File reception canceled by user: {file_name}")
                    else:
                        display_message(chat_box, "Other", f"File reception canceled by user: {file_name}")
                else:
                    message = client_socket.recv(1024).decode('utf-8')

                    decrypted_message = aes_decrypt(message, aes_key)

                    if message and message != "Channel joined successfully.":
                        display_message(chat_box, user, decrypted_message)
            except Exception as e:
                print("Erreur de réception des messages:", e)
                break

    receive_thread = threading.Thread(target=receive_messages, args=(aes_key,))
    receive_thread.daemon = True
    receive_thread.start()

    def upload_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            display_message(chat_box, "Moi", f"File uploaded: {file_path}")
            try:
                file_size = os.path.getsize(file_path)
                with open(file_path, "rb") as file:
                    file_data = file.read()
                    client_socket.sendall(b"FILE")
                    client_socket.sendall(username)
                    client_socket.sendall(f"{os.path.basename(file_path):<100}".encode('utf-8'))
                    client_socket.sendall(f"{file_size:<100}".encode('utf-8'))
                    client_socket.sendall(file_data)
                print("Transfert de fichier terminé.")
            except Exception as e:
                print("Erreur lors de l'envoi du fichier:", e)

    upload_button = ctk.CTkButton(input_frame, text="Upload File", command=upload_file)
    upload_button.pack(side=tk.LEFT, padx=10, pady=5)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
