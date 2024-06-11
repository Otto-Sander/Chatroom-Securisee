"""
login_window.py
--------------------------------------------------------------------------------------------------------------
Ce fichier contient la définition de la classe LoginWindow, qui crée l'interface utilisateur graphique 
pour la connexion à la chatroom. 
La fenêtre permet aux utilisateurs de se connecter avec leurs identifiants ou de créer un nouveau compte.

Les utilisateurs peuvent également se connecter à une salle de chat après une authentification réussie.
--------------------------------------------------------------------------------------------------------------
Fonctionnalités :
- Affichage d'un message de bienvenue.
- Formulaire de connexion avec nom d'utilisateur et mot de passe.
- Options pour se connecter ou créer un nouveau compte.
- Connexion à une salle de chat sécurisée après l'authentification.
"""
from PIL import Image,ImageTk
from tkinter import *
import tkinter as tk
from open_chatroom import open_chatroom
from PIL import ImageTk, Image

# Définition des polices
head1 = ("Lexend", 18, "bold") 
head2 = ("Lexend", 14, "italic")
head3 = ("Lexend", 12, "bold")
head4_button = ("Lexend", 9)

#Fonction permettant de retourner les coordonnées du milieu de la fenêtre
def return_center_coord(self):
    window_width = 600
    window_height = 500

    # get the screen dimension
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    
    return window_width, window_height, center_x, center_y

#Classe principale de login
class LoginWindow:
    #Introduction
    def __init__(self, master):
        self.master = master
        self.master.title("Authentification")

        window_width, window_height, center_x, center_y = return_center_coord(self)

        # set the position of the window to the center of the screen
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Cadre principal
        self.frame = tk.Frame(master)
        self.frame.configure(background='#152242')
        self.frame.pack(padx=40, pady=40)
        
        # Texte de bienvenue
        self.welcome_label = tk.Label(self.frame, justify="left", font=head1, text="Bonjour et bienvenue dans notre application sécurisée de Data Room Virtuelle !", wraplength=500, pady=30, fg="white")
        self.welcome_label.configure(background='#152242')
        self.welcome_label.pack(pady=5)
        self.welcome_label_2 = tk.Label(self.frame, justify="left", font=head2, text="Nous sommes ravis de vous avoir parmi nous !", wraplength=500, pady=30, fg="white")
        self.welcome_label_2.configure(background='#152242')
        self.welcome_label_2.pack(pady=5)

        self.login_button = tk.Button(self.frame, text="Suivant", command=self.show_authentication, font=head4_button)
        self.login_button.pack(side=tk.RIGHT, anchor=tk.SE, pady=60)

    #Connection panel : login
    def show_authentication(self):
        self.welcome_label.destroy()
        self.welcome_label_2.destroy()
        self.login_button.destroy()

        # Texte de bienvenue
        self.enter_info = tk.Label(self.frame, justify="left", font=head2, text="Veuillez vous connecter avec vos identifiants pour accéder à l'espace de chat et de partage de documents.\n", wraplength=400, fg="white")
        self.enter_info.configure(background='#152242')
        self.enter_info.pack(pady=5)

        # Éléments du formulaire de connexion
        self.username_label = tk.Label(self.frame, font=head3, text="Nom d'utilisateur:", bg='#152242', fg="white")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.frame, font=head3, text="Mot de passe:", bg='#152242', fg="white")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5) 

        self.login_button = tk.Button(self.frame, text="Se connecter", command=self.authenticate, font=head4_button)
        self.login_button.pack(pady=5)
        self.subscribe_button = tk.Button(self.frame, text="Créer un compte", command=self.show_create_user, font=head4_button)
        self.subscribe_button.pack(pady=5)

    #Connection panel : create user
    def show_create_user(self):
        self.frame.destroy()
        
        self.frame = tk.Frame(self.master)
        self.frame.configure(background='#152242')
        self.frame.pack(padx=40, pady=40)

        self.create_user_label = tk.Label(self.frame, justify="left", font=head2, text="Créer un nouveau compte utilisateur", wraplength=400, fg="white")
        self.create_user_label.configure(background='#152242')
        self.create_user_label.pack(pady=5)

        self.new_username_label = tk.Label(self.frame, font=head3, text="Nom d'utilisateur:", bg='#152242', fg="white")
        self.new_username_label.pack(pady=5)
        self.new_username_entry = tk.Entry(self.frame)
        self.new_username_entry.pack(pady=5)

        self.new_password_label = tk.Label(self.frame, font=head3, text="Mot de passe:", bg='#152242', fg="white")
        self.new_password_label.pack(pady=5)
        self.new_password_entry = tk.Entry(self.frame, show="*")
        self.new_password_entry.pack(pady=5)

        self.confirm_password_label = tk.Label(self.frame, font=head3, text="Confirmer le mot de passe:", bg='#152242', fg="white")
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.frame, show="*")
        self.confirm_password_entry.pack(pady=5)

        self.create_account_button = tk.Button(self.frame, text="Créer un compte", command=self.create_user, font=head4_button)
        self.create_account_button.pack(pady=5)
        self.back_to_login_button = tk.Button(self.frame, text="Retour", command=self.back_to_login, font=head4_button)
        self.back_to_login_button.pack(pady=5)

    #Connection panel : back to login
    def back_to_login(self):
        # Efface le contenu du cadre
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Affiche à nouveau le formulaire d'authentification
        self.show_authentication()

    #ALERT : Create User failed
    def create_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
        elif new_username == "" or new_password == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        else:
            # Enregistrer le nouvel utilisateur (code à implémenter)
            # Par exemple, vous pouvez enregistrer les informations dans une base de données ou un fichier.
            messagebox.showinfo("Succès", "Compte créé avec succès !")
            self.back_to_login()

    #ALERT : Create Connection failed
    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            self.frame.destroy()  # Fermer l'ancienne interface
            self.show_config()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    #SHOW : Confiration Connection
    def show_config(self):
        self.frame.destroy()

        self.frame = tk.Frame(self.master)
        self.frame.configure(background='#152242')
        self.frame.pack(padx=40, pady=100)

        self.ip_label = tk.Label(self.frame, text="Adresse IP du serveur:", bg='#152242', fg="white")
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(self.frame)
        self.ip_entry.pack(pady=5)
        
        self.port_label = tk.Label(self.frame, text="Port:", bg='#152242', fg="white")
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(self.frame)
        self.port_entry.pack(pady=5)
        
        self.connect_button = tk.Button(self.frame, text="Connecter", command=self.connect_chatroom, font=head4_button)
        self.connect_button.pack(pady=5)

    #ALERT : Connection Success
    def connect_chatroom(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        # Code pour connecter à la chatroom en utilisant l'adresse IP et le port fournis
        messagebox.showinfo("Info", "Connecté à la chatroom avec succès.")
        self.master.destroy()
        open_chatroom()
