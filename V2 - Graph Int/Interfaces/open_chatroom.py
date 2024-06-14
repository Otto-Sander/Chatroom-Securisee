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

def open_chatroom(self):
    self.frame.destroy()

    self.title("Data Room Virtuelle")

    # Créer une zone de chat
    chat_box = tk.Text(self.frame, state=tk.DISABLED)
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