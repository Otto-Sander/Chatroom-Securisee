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
import random
import string

# ------------------------ Graphic DESIGN ------------------------------------------------------
cadre = '#0A1A29'
back = '#1A1E88'
letter = 'white'
letter_button = 'white'
button = '#1821BD'
hover_button="#C9511D"
# ----------------------------------------------------------------------------------------------

# Définition des polices
head1 = ("Lexend", 25, "bold") 
head2 = ("Lexend", 19)
head3 = ("Lexend", 15)
head4 = ("Lexend", 11)
head4_button = ("Lexend", 9)

#Classe principale de login
class LoginWindow:
    #Introduction
    def __init__(self, master):
        self.master = master
        self.master.title("Authentification")

        self.frame = CTkFrame(self.master,width=950,height=600,corner_radius=30,fg_color=cadre,bg_color='#1A324C')
        self.frame.place(x=200,y=70)
    

        #Introduction : 1 --------------------------------------------------
        txt = "Welcome to our\nSecure Virtual Data Room application!"
        self.heading_1 = Label(self.frame, text=txt, font=head1, bg=cadre, fg=letter, justify=LEFT,anchor="w")
        self.heading_1.place(relx=0.38, rely=0.15, anchor=tk.CENTER)

        # Introduction : 2 -------------------------------------------------
        txt_intro2 = "We're delighted to have you with us!"
        self.heading_2 = Label(self.frame, text=txt_intro2, font=head2, bg=cadre, fg=letter, justify=LEFT,anchor="w")
        self.heading_2.place(relx=0.067, rely=0.225, width=500, height=50)

        # Left Image ----------------------------------------
        image_path = "Images\logo.jpg"
        image = Image.open(image_path)
        image = image.resize((310,230))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0)
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=73, y=230)

        # Right Text - Presentation ------------------------------
        txt_intro3 = "MasterCamp is your secure space to share documents\nand chat with complete confidentiality.Protect your\nexchanges with our encrypted communication and\ndetailed access management. Simplify your\nsensitive projects with MasterCamp!"
        self.heading_3 = Label(self.frame, text=txt_intro3, font=head3, bg=cadre, fg=letter, justify=LEFT,anchor="w")
        self.heading_3.place(relx=0.45, rely=0.32, width=400, height=200)

        # BOUTON-------------------------------------------
        button = Image.open("Images\logo_next.png")
        resized_image = button.resize((70, 70))
        # Convertir l'image redimensionnée en format ImageTk.PhotoImage
        image = ImageTk.PhotoImage(resized_image)
        # Créer le bouton avec l'image redimensionnée
        self.roundedbutton = tk.Button(self.frame, image=image, bd=0, borderwidth=0,bg=cadre,command=self.show_authentication)
        self.roundedbutton.image = image  # Gardez une référence à l'image pour éviter la collecte des déchets
        self.roundedbutton.place(x=720, y=450)
        #-----------------------------------------------------

    #Connection panel : login ------------------------------------------------------
    def show_authentication(self):
        self.frame.destroy()

        # Cadre principal ------------------------------------------------
        self.frame = CTkFrame(self.master,width=950,height=600,corner_radius=30,fg_color=cadre,bg_color='#1A324C')
        self.frame.place(x=200,y=70)

        # Title ---------------------------------------------------------
        head = "Authentication"
        self.heading_1 = Label(self.frame, text=head, font=head1, bg=cadre, fg=letter, justify=LEFT,anchor="nw")
        self.heading_1.place(relx=0.065, rely=0.08, width=1000, height=100)


        #Introduction : 1 -----------------------------------------
        txt = "Please log in with\nyour login details to access the chat and document sharing area."
        self.heading_1 = Label(self.frame, text=txt, font=head2, bg=cadre, fg=letter, justify=LEFT,anchor="nw")
        self.heading_1.place(relx=0.065, y=90, width=1000, height=100)

        # GIF Animation Star ------------------------------------------
        gif_path = 'videos/star_effect.gif'

        def get_frames(gif_path):
            frames = []
            with Image.open(gif_path) as img:
                try:
                    while True:
                        frame = img.copy().convert("RGBA")
                        frame = frame.resize((280, 280))
                        frames.append(ImageTk.PhotoImage(frame))
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass
            return frames

        frames = get_frames(gif_path)
        frameCnt = len(frames)

        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            gif_label.configure(image=frame, bg=cadre)
            self.frame.after(90, update, ind)

        gif_label = Label(self.frame, bg=cadre)
        gif_label.place(x=182, y=180)  # Positionnement du GIF
        self.frame.after(0, update, 0)

        # Left Image ----------------------------------------------
        image_path = "Images\login_interface.png"
        image = Image.open(image_path)
        image = image.resize((260,260))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0,bg=cadre)
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=110, y=250)

        # User Image Panel ----------------------------------------------------
        image = Image.open("Images\\user.png")
        image = image.resize((60,60))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0,bg=cadre)
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=620, y=190)

        # Sign Up Label -------------------------------------------------
        self.sign_in_label = Label(self.frame, text='Sign In',bg=cadre,fg=letter,font=head4)
        self.sign_in_label.place(x=624, y=255)

        # Username ------------------------------------------------------
        self.username_label = Label(self.frame, text='Username', bg=cadre, font=('yu gothic ui', 13, 'bold'),fg=letter)
        self.username_label.place(x=500, y=280)
        self.username_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg=cadre, fg='#D4D4D4',font=('yu gothic ui', 12))
        self.username_entry.place(x=525, y=312, width=270)
        self.username_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.username_line.place(x=500, y=339)

        # User laber logo ----------------------------------------------
        username_icon = Image.open('images/user_label.png')
        resized_icon = username_icon.resize((20, 20))
        photo_user = ImageTk.PhotoImage(resized_icon)
        self.username_icon_label = Label(self.frame, image=photo_user, bg=cadre)
        self.username_icon_label.image = photo_user
        self.username_icon_label.place(x=500, y=312)

        # Password ------------------------------------------------------
        self.passwd_label = Label(self.frame, text='Password', bg=cadre, font=('yu gothic ui', 13, 'bold'),fg=letter)
        self.passwd_label.place(x=500, y=350)
        self.passwd_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg=cadre, fg='#D4D4D4',font=('yu gothic ui', 12),show="*")
        self.passwd_entry.place(x=525, y=383, width=270)
        self.passwd_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.passwd_line.place(x=500, y=410)

        # Password laber logo ----------------------------------------------
        passwd_icon = Image.open('images/lock.png')
        resized_icon = passwd_icon.resize((20, 20))
        photo_passwd = ImageTk.PhotoImage(resized_icon)
        self.passwd_icon_label = Label(self.frame, image=photo_passwd, bg=cadre)
        self.passwd_icon_label.image = photo_passwd
        self.passwd_icon_label.place(x=500, y=383)

        # Login Button ------------------------------------
        button = CTkButton(master=self.frame,text='Login',corner_radius=32,fg_color='#4158D0',hover_color='#C850C0',width=300,font=head3,command=self.authenticate)
        button.place(x=500,y=435)

        # No account Label ---------------------------------------
        self.sign_label = Label(self.frame, text='No account yet?', font=('yu gothic ui', 11, 'bold'),background=cadre, fg=letter)
        self.sign_label.place(x=500, y=490)

        # Create Account Button ------------------------------------
        button = CTkButton(master=self.frame,text='Create Account',corner_radius=32,fg_color='#318A4C',hover_color='#C850C0',width=200,font=head3,command=self.show_create_user)
        button.place(x=500,y=520)

    #Connection panel : create user
    def show_create_user(self):
        self.frame.destroy()  # Supprimer le cadre actuel

        # Cadre principal ------------------------------------------------
        self.frame = CTkFrame(self.master,width=950,height=600,corner_radius=30,fg_color=cadre,bg_color='#1A324C')
        self.frame.place(x=200,y=70)

        # Title ---------------------------------------------------------
        head = "Account Creation"
        self.heading_1 = Label(self.frame, text=head, font=head1, bg=cadre, fg=letter, justify=LEFT,anchor="nw")
        self.heading_1.place(relx=0.065, rely=0.08, width=1000, height=100)


        #Introduction : 1 -----------------------------------------
        txt = "Join us today to enjoy exclusive benefits and stay updated!"
        self.heading_1 = Label(self.frame, text=txt, font=head2, bg=cadre, fg=letter, justify=LEFT,anchor="nw")
        self.heading_1.place(relx=0.065, y=90, width=1000, height=100)

        # GIF Animation Star ------------------------------------------
        gif_path = 'videos/create_account.gif'

        def get_frames(gif_path):
            frames = []
            with Image.open(gif_path) as img:
                try:
                    while True:
                        frame = img.copy().convert("RGBA")
                        frame = frame.resize((190, 190))
                        frames.append(ImageTk.PhotoImage(frame))
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass
            return frames

        frames = get_frames(gif_path)
        frameCnt = len(frames)

        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt-30:
                ind = 0
            gif_label.configure(image=frame, bg=cadre)
            self.frame.after(70, update, ind)

        gif_label = Label(self.frame, bg=cadre)
        gif_label.place(x=150, y=220)  # Positionnement du GIF
        self.frame.after(0, update, 0)

        # User Image Panel ----------------------------------------------------
        image = Image.open("Images\\user.png")
        image = image.resize((60,60))
        image = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=image,borderwidth=0,bg=cadre)
        label.image = image  # Référence nécessaire pour empêcher la collecte des déchets
        label.place(x=620, y=160)

        # Sign Up Label -------------------------------------------------
        self.sign_in_label = Label(self.frame, text='Sign In',bg=cadre,fg=letter,font=head4)
        self.sign_in_label.place(x=624, y=225)

        # Username ------------------------------------------------------
        self.username_label = Label(self.frame, text='Username', bg=cadre, font=('yu gothic ui', 13, 'bold'),fg=letter)
        self.username_label.place(x=500, y=250)
        self.username_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg=cadre, fg='#D4D4D4',font=('yu gothic ui', 12))
        self.username_entry.place(x=525, y=282, width=270)
        self.username_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.username_line.place(x=500, y=309)

        # User laber logo ----------------------------------------------
        username_icon = Image.open('images/user_label.png')
        resized_icon = username_icon.resize((20, 20))
        photo_user = ImageTk.PhotoImage(resized_icon)
        self.username_icon_label = Label(self.frame, image=photo_user, bg=cadre)
        self.username_icon_label.image = photo_user
        self.username_icon_label.place(x=500, y=282)

        # Password ------------------------------------------------------
        self.passwd_label = Label(self.frame, text='Password', bg=cadre, font=('yu gothic ui', 13, 'bold'),fg=letter)
        self.passwd_label.place(x=500, y=320)
        self.passwd_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg=cadre, fg='#D4D4D4',font=('yu gothic ui', 12),show="*")
        self.passwd_entry.place(x=525, y=353, width=270)
        self.passwd_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.passwd_line.place(x=500, y=380)

        # Password laber logo ----------------------------------------------
        passwd_icon = Image.open('images/lock.png')
        resized_icon = passwd_icon.resize((20, 20))
        photo_passwd = ImageTk.PhotoImage(resized_icon)
        self.passwd_icon_label = Label(self.frame, image=photo_passwd, bg=cadre)
        self.passwd_icon_label.image = photo_passwd
        self.passwd_icon_label.place(x=500, y=353)

        # Confirm Password ------------------------------------------------------
        self.passwd_label = Label(self.frame, text='Confirm Password', bg=cadre, font=('yu gothic ui', 13, 'bold'),fg=letter)
        self.passwd_label.place(x=500, y=390)
        self.confirm_passwd_entry = Entry(self.frame, highlightthickness=0, relief=FLAT, bg=cadre, fg='#D4D4D4',font=('yu gothic ui', 12),show="*")
        self.confirm_passwd_entry.place(x=525, y=413, width=270)
        self.passwd_line = Canvas(self.frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.passwd_line.place(x=500, y=450)

        # Confirm Password laber logo ----------------------------------------------
        passwd_icon = Image.open('images/lock.png')
        resized_icon = passwd_icon.resize((20, 20))
        photo_passwd = ImageTk.PhotoImage(resized_icon)
        self.passwd_icon_label = Label(self.frame, image=photo_passwd, bg=cadre)
        self.passwd_icon_label.image = photo_passwd
        self.passwd_icon_label.place(x=500, y=413)

        # Login Button ------------------------------------
        button = CTkButton(master=self.frame,text='Create',corner_radius=32,fg_color='#4158D0',hover_color='#C850C0',width=300,font=head3,command=self.authenticate)
        button.place(x=500,y=475)

        # BOUTON-------------------------------------------
        button = Image.open("Images\logo_next_before.png")
        resized_image = button.resize((60, 60))
        # Convertir l'image redimensionnée en format ImageTk.PhotoImage
        image = ImageTk.PhotoImage(resized_image)
        # Créer le bouton avec l'image redimensionnée
        self.roundedbutton = tk.Button(self.frame, image=image, bd=0, borderwidth=0,bg=cadre,command=self.show_authentication)
        self.roundedbutton.image = image  # Gardez une référence à l'image pour éviter la collecte des déchets
        self.roundedbutton.place(relx=0.065, y=450)
        #-----------------------------------------------------

    #Connection panel : back to login
    def back_to_login(self):
        # Efface le contenu du cadre
        self.frame.destroy()
        # Affiche à nouveau le formulaire d'authentification
        self.show_authentication()


    #ALERT : Create User failed
    def create_user(self):
        new_username = self.username_entry.get()
        new_password = self.passwd_entry.get()
        confirm_password = self.confirm_passwd_entry.get()

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
        self.frame = CTkFrame(self.master,width=950,height=600,corner_radius=30,fg_color=cadre,bg_color='#1A324C')
        self.frame.place(x=200,y=70)

        self.label = tk.Label(self.frame, text="To connect with your friends, enter their code or generate a new one.", font=head2, bg=cadre, fg=letter)
        self.label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        self.enter_code_label = tk.Label(self.frame, text="Enter room code", font=head1, bg=cadre, fg=letter)
        self.enter_code_label.place(relx=0.5, rely=0.22, anchor=tk.CENTER)
        code_entry = CTkEntry(master=self.frame, corner_radius=20, fg_color='black', text_color=letter, width=200, height=55, font=('Lexend', 30))
        code_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        button_join = CTkButton(master=self.frame, text='Join a room', corner_radius=32, fg_color=button, hover_color=hover_button,text_color=letter_button, width=200, font=('Lexend', 30, 'bold'), command=self.show_config)
        button_join.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.or_label = tk.Label(self.frame, text="or", font=('Lexend', 20), bg=cadre, fg=letter)
        self.or_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.button_generate = CTkButton(master=self.frame, text='Generate a code', corner_radius=32,fg_color=button, hover_color=hover_button, width=200, text_color=letter_button,font=('Lexend', 30, 'bold'), command=self.generate_code)
        self.button_generate.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.code_label = tk.Label(self.frame, text="", font=('Lexend', 30), bg=cadre, fg='white')
        self.code_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def generate_code(self):
        # Générer un code aléatoire de 8 caractères
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.code_label.config(text=code)
        print("Code généré:", code)  # Debugging

        # Supprimer le bouton existant
        self.button_generate.destroy()

        # Créer un nouveau bouton avec le texte et la commande mis à jour
        self.button_enter_room = CTkButton(master=self.frame, text='Enter room', corner_radius=32, fg_color=button, text_color=letter_button,
                                           hover_color=hover_button, width=200, font=('Lexend', 30, 'bold'),
                                           command=self.connect_chatroom)
        self.button_enter_room.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    #ALERT : Connection Success
    def connect_chatroom(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        # Code pour connecter à la chatroom en utilisant l'adresse IP et le port fournis
        tk.messagebox.showinfo("Info", "Connecté à la chatroom avec succès.")
        self.master.destroy()
        open_chatroom()
