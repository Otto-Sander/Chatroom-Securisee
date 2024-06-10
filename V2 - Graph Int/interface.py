import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

head1 = ("Lexend", 15, "bold") 
head2 = ("Lexend", 11, "italic")
head3 = ("Lexend", 9, "bold")
head4_button = ("Lexend", 9)

def return_center_coord(self):

    window_width = 600
    window_height = 500

    # get the screen dimension
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    
    return window_height,window_height,center_x,center_y



class LoginWindow:
    def __init__(self, master):
        
        self.master = master
        self.master.title("Authentification")

        window_width,window_height,center_x,center_y = return_center_coord(self)

        # set the position of the window to the center of the screen
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Cadre principal
        self.frame = tk.Frame(master)
        self.frame.configure(background='#152242')
        self.frame.pack(padx=40, pady=40)
        
        # Texte de bienvenue
        self.welcome_label = tk.Label(self.frame, justify="left", font=head1, text="Bonjour et bienvenue dans notre application sécurisée de Data Room Virtuelle !", wraplength=500,pady=30, fg="white")
        self.welcome_label.configure(background='#152242')
        self.welcome_label.pack(pady=5)
        self.welcome_label_2 = tk.Label(self.frame, justify="left", font=head2, text="Nous sommes ravis de vous avoir parmi nous !", wraplength=500,pady=30, fg="white")
        self.welcome_label_2.configure(background='#152242')
        self.welcome_label_2.pack(pady=5)

        self.login_button = tk.Button(self.frame, text="Suivant", command=self.show_authentication,font=head4_button)
        self.login_button.pack(side=tk.RIGHT, anchor=tk.SE, pady=60) 

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
        self.login_button = tk.Button(self.frame, text="Se connecter", command=self.authenticate,font=head4_button)
        self.login_button.pack(pady=5)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            self.frame.destroy()  # Fermer l'ancienne interface
            self.show_config()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def show_config(self):
        # Créer les éléments de configuration
        #self.block = tk.Canvas(self.master, width=200, height=200,bg="#152242")
        #self.block.pack(pady=10)

        self.ip_label = tk.Label(self.master, text="Adresse IP du serveur:")
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.pack(pady=5)
        self.port_label = tk.Label(self.master, text="Port:")
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(self.master)
        self.port_entry.pack(pady=5)
        self.connect_button = tk.Button(self.master, text="Connecter", command=self.connect_chatroom)
        self.connect_button.pack(pady=5)

    def connect_chatroom(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        # Code pour connecter à la chatroom en utilisant l'adresse IP et le port fournis
        messagebox.showinfo("Info", "Connecté à la chatroom avec succès.")
        self.master.destroy()
        open_chatroom()

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
            display_message(chat_box, "Moi", message)
            message_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Attention", "Veuillez saisir un message.")

    def display_message(chat_box, user, message):
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"{user}: {message}\n")
        chat_box.config(state=tk.DISABLED)
        chat_box.see(tk.END)

    root.mainloop()

def main():
    login_root = tk.Tk()
    login_root.configure(background='#152242')

    login_root.eval('tk::PlaceWindow . center')
    login_window = LoginWindow(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    main()
