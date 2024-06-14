import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import datetime

def open_chatroom():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    window_width = 600
    window_height = 600

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.title("Data Room Virtuelle")

    # Create a frame for the chat
    chat_frame = ctk.CTkFrame(root)
    chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create a chat box
    chat_box = ctk.CTkTextbox(chat_frame, state=tk.DISABLED, wrap=tk.WORD)
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create a frame for the message entry and send button
    input_frame = ctk.CTkFrame(root)
    input_frame.pack(padx=10, pady=5, fill=tk.X)

    # Create a message entry box
    message_entry = ctk.CTkEntry(input_frame, placeholder_text="Écrire un message...")
    message_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)

    # Create a send button
    send_button = ctk.CTkButton(input_frame, text="Envoyer", command=lambda: send_message(chat_box, message_entry))
    send_button.pack(side=tk.LEFT, padx=10, pady=5)

    def send_message(chat_box, message_entry):
        message = message_entry.get()
        if message:
            # Code to send the message securely
            display_message(chat_box, "Moi", message)
            message_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Attention", "Veuillez saisir un message.")

    def display_message(chat_box, user, message):
        current_time = datetime.datetime.now()
        current_time_string = current_time.strftime("%H:%M")

        if user == "Moi":
            bg_color = "#222222"  # Gris foncé pour l'utilisateur actuel
            text_color = "#FFFFFF"
        else:
            bg_color = "#333333"  # Gris clair pour les autres utilisateurs
            text_color = "#FFFFFF"

        chat_box.configure(state=tk.NORMAL)
        chat_box.tag_config("user", background=bg_color, foreground=text_color)
        chat_box.insert(tk.END, f"({current_time_string}) {user}: {message}\n", "user")
        chat_box.configure(state=tk.DISABLED)
        chat_box.see(tk.END)

    root.mainloop()

