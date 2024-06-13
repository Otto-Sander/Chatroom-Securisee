"""
open_chatroom.py
-----------------------------------------------------------------------------------------------------------------
Ce fichier contient la fonction open_chatroom qui crée et ouvre une fenêtre de chat pour une application de Data 
Room Virtuelle. La salle de chat permet aux utilisateurs de communiquer en envoyant et recevant des messages. 
-----------------------------------------------------------------------------------------------------------------
Fonctionnalités :
- Création d'une fenêtre de chat centrée sur l'écran.
- Zone de texte pour afficher les messages reçus et envoyés.
- Champ de saisie pour écrire des messages.
- Bouton pour envoyer des messages.
- Affichage des messages envoyés dans la zone de texte.
"""

import tkinter as tk
from tkinter import messagebox
import datetime

def open_chatroom():
    root = tk.Tk()
    window_width = 600
    window_height = 600

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.title("Data Room Virtuelle")

    # Créer une zone de chat
    chat_box = tk.Text(root, state=tk.DISABLED)
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Créer une zone de saisie de message
    message_entry = tk.Entry(root)
    message_entry.pack(padx=10, pady=5, fill=tk.X)

    # Créer un bouton pour envoyer le message
    send_button = tk.Button(root, text="Envoyer", command=lambda: send_message(chat_box, message_entry))
    send_button.pack(padx=10, pady=5)

    def send_message(chat_box, message_entry):
        message = message_entry.get()
        if message:
            # Code pour envoyer le message de manière sécurisée
            display_message(chat_box,"Moi", message)
            message_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Attention", "Veuillez saisir un message.")

    #Affiche le message
    def display_message(chat_box, user, message):
        currentime = datetime.datetime.now()
        currentime_string = currentime.strftime("%H:%M:%S")

        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"({currentime_string}){user}: {message}\n")
        chat_box.config(state=tk.DISABLED)
        chat_box.see(tk.END)

    root.mainloop()