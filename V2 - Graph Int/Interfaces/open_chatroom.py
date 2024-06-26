import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import threading
import socket
from DB_main import supabase
from DB_CRUD_Functions import *
from Auth import *
import os
import time

client_socket = None

def open_chatroom(previous_win, width_win, height_win, code, username):

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

    message_entry.bind("<Return>", lambda event: send_message(chat_box, message_entry, client_socket))

    try:
        ip, port = get_last_server(supabase)
        user_id = get_current_connected_user_id(supabase)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.send(code.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')

        user_id_str = str(user_id)
        client_socket.send(user_id_str.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de se connecter au serveur : {e}")
        on_close()
        return

    def send_message(chat_box, message_entry, client):
        message = message_entry.get()
        if message:
            try:
                client.send(message.encode('utf-8'))
                display_message(chat_box, "Moi", message)
                message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'envoyer le message : {e}")
        else:
            messagebox.showwarning("Attention", "Veuillez saisir un message.")

    def display_message(chat_box, user, message):
        current_time = datetime.datetime.now()
        current_time_string = current_time.strftime("%H:%M")

        if user == "Moi":
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

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message and message != "Channel joined successfully.":
                    display_message(chat_box, "Autre", message)
            except Exception as e:
                print("Erreur de réception des messages:", e)
                break

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    def upload_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            file_size = os.path.getsize(file_path)
            with open(file_path,"rb") as file:
                # Starting the time capture
                start_time = time.time()
                file_data = file.read()

                # Chiffrement du fichier ----------------------------------------

                # ---------------------------------------------------------------
                client_socket.sendall("FILE".encode())
                client_socket.sendall(f"{os.path.basename(file_path):<100}".encode('utf-8'))
                client_socket.sendall(f"{len(file_data):<100}".encode('utf-8'))

            display_message(chat_box, "Moi", f"File uploaded: {file_path}")


    upload_button = ctk.CTkButton(input_frame, text="Upload File", command=upload_file)
    upload_button.pack(side=tk.LEFT, padx=10, pady=5)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    # FILE 
    def receive_file():
        if not os.path.exists("temp"):
            os.makedirs("temp")

        file_name = client_socket.recv(100).decode().strip()
        file_size = int(client_socket.recv(100).decode().strip())

        encoded_file_data = b""
        while len(encoded_file_data) < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            encoded_file_data += data

        # Déchiffrement du fichier -----------------------------------------------

        #-------------------------------------------------------------------------

        with open(os.path.join("temp", file_name), "wb") as file:
            file.write(encoded_file_data)

        print("Transfert de fichier terminé.")
