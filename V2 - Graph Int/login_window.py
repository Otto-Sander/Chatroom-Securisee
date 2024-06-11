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
from customtkinter import *

# Définition des polices
head1 = ("Lexend", 18, "bold") 
head2 = ("Lexend", 14)
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

        # Cadre principal ------------------------------------------------
        self.frame = tk.Frame(self.master,bg='#152242',width=950,height=600)
        self.frame.place(x=200,y=70)

        #Introduction : 1 --------------------------------------------------
        txt = "Bonjour et bienvenue \ndans notre application sécurisée de Data Room Virtuelle !"
        self.heading_1 = Label(self.frame, text=txt, font=head1, bg='#152242', fg='white', justify=LEFT)
        self.heading_1.place(x=60, y=30, width=800, height=200)

        # Introduction : 2 -------------------------------------------------
        txt_intro2 = "Nous sommes ravis de vous avoir parmi nous !"
        self.heading_2 = Label(self.frame, text=txt_intro2, font=head2, bg='#152242', fg='white', justify=LEFT)
        self.heading_2.place(x=0, y=180, width=680, height=50)

        # Left Image ----------------------------------------
        image_path = "Images\Logo.jpeg"
        image = Image.open(image_path)
        image = image.resize((230,230))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0)
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=140, y=300)

        # BOUTON-------------------------------------------
        button = Image.open("Images\logo_next.png")
        resized_image = button.resize((90, 90))
        # Convertir l'image redimensionnée en format ImageTk.PhotoImage
        image = ImageTk.PhotoImage(resized_image)
        # Créer le bouton avec l'image redimensionnée
        self.roundedbutton = tk.Button(self.frame, image=image, bd=0, borderwidth=0,bg="#152242",command=self.show_authentication)
        self.roundedbutton.image = image  # Gardez une référence à l'image pour éviter la collecte des déchets
        self.roundedbutton.place(x=700, y=480)
        #-----------------------------------------------------

    #Connection panel : login ------------------------------------------------------
    def show_authentication(self):
        self.frame.destroy()
        # Cadre principal ---------------------------------------
        self.frame = tk.Frame(self.master,bg='#152242',width=950,height=600)
        self.frame.place(x=200,y=70)

        #Introduction : 1 -----------------------------------------
        txt = "Veuillez vous connecter avec vos identifiants pour\naccéder à l'espace de chat et de partage de documents."
        self.heading_1 = Label(self.frame, text=txt, font=head1, bg='#152242', fg='white', justify=LEFT)
        self.heading_1.place(x=60, y=30, width=800, height=200)

        # Left Image ----------------------------------------------
        image_path = "Images\login_interface.png"
        image = Image.open(image_path)
        image = image.resize((280,280))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0,bg='#152242')
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=140, y=250)

        # User Image Panel ----------------------------------------------------
        image = Image.open("Images\\user.png")
        image = image.resize((60,60))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0,bg='#152242')
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=600, y=190)

        # Sign Up Label -------------------------------------------------
        self.sign_in_label = Label(self.frame, text='Sign In',bg='#152242',fg='white',font=head2)
        self.sign_in_label.place(x=598, y=255)

        # Username ------------------------------------------------------
        self.username_label = Label(self.frame, text='Username', bg='#152242', font=('yu gothic ui', 13, 'bold'),fg='white')
        self.username_label.place(x=500, y=300)
        self.username_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg='#152242', fg='white',
        font=('yu gothic ui', 12, 'bold'))
        self.username_entry.place(x=525, y=332, width=270)
        self.username_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.username_line.place(x=500, y=359)

        # User laber logo ----------------------------------------------
        username_icon = Image.open('images/user_label.png')
        resized_icon = username_icon.resize((20, 20))
        photo_user = ImageTk.PhotoImage(resized_icon)
        self.username_icon_label = Label(self.frame, image=photo_user, bg='#152242')
        self.username_icon_label.image = photo_user
        self.username_icon_label.place(x=500, y=332)

        # Password ------------------------------------------------------
        self.passwd_label = Label(self.frame, text='Password', bg='#152242', font=('yu gothic ui', 13, 'bold'),fg='white')
        self.passwd_label.place(x=500, y=370)
        self.passwd_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg='#152242', fg='white',
        font=('yu gothic ui', 12, 'bold'),show="*")
        self.passwd_entry.place(x=525, y=403, width=270)
        self.passwd_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.passwd_line.place(x=500, y=430)

        # Password laber logo ----------------------------------------------
        passwd_icon = Image.open('images/user_label.png')
        resized_icon = passwd_icon.resize((20, 20))
        photo_passwd = ImageTk.PhotoImage(resized_icon)
        self.passwd_icon_label = Label(self.frame, image=photo_passwd, bg='#152242')
        self.passwd_icon_label.image = photo_passwd
        self.passwd_icon_label.place(x=500, y=403)

        # Login Button ------------------------------------
        button = CTkButton(master=self.frame,text='Login',corner_radius=32,fg_color='#4158D0',hover_color='#C850C0',width=300,font=head3,command=self.authenticate)
        button.place(x=500,y=455)

        # No account Label ---------------------------------------
        self.sign_label = Label(self.frame, text='No account yet?', font=('yu gothic ui', 11, 'bold'),background="#152242", fg='white')
        self.sign_label.place(x=500, y=490)

        # Create Account Button ------------------------------------
        button = CTkButton(master=self.frame,text='Create Account',corner_radius=32,fg_color='#2BB069',hover_color='#C850C0',width=200,font=head3,command=self.show_create_user)
        button.place(x=500,y=520)

    #Connection panel : create user
    def show_create_user(self):
        self.frame.destroy()  # Supprimer le cadre actuel
        
        # Cadre principal ---------------------------------------
        self.frame = tk.Frame(self.master,bg='#152242',width=950,height=600)
        self.frame.place(x=200,y=70)

        self.create_user_label = tk.Label(self.frame, justify="left", font=head2, text="Créer un nouveau compte utilisateur", wraplength=400, fg="white", bg='#152242')
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
        self.frame.destroy()
        # Affiche à nouveau le formulaire d'authentification
        self.show_authentication()


    #ALERT : Create User failed
    def create_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            tk.messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
        elif new_username == "" or new_password == "":
            tk.messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        else:
            # Enregistrer le nouvel utilisateur (code à implémenter)
            # Par exemple, vous pouvez enregistrer les informations dans une base de données ou un fichier.
            tk.messagebox.showinfo("Succès", "Compte créé avec succès !")
            self.back_to_login()  # Retour à la page de connexion après la création de compte


    #ALERT : Create Connection failed
    def authenticate(self):
        username = self.username_entry.get()
        password = self.passwd_entry.get()
        if username == "admin" and password == "admin":
            self.frame.destroy()  # Fermer l'ancienne interface
            self.show_config()
        else:
            tk.messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    #SHOW : Confiration Connection
    def show_config(self):
        self.frame.destroy()

        # Cadre principal ---------------------------------------
        self.frame = tk.Frame(self.master,bg='#152242',width=950,height=600)
        self.frame.place(x=200,y=70)

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
        tk.messagebox.showinfo("Info", "Connecté à la chatroom avec succès.")
        self.master.destroy()
        open_chatroom()
