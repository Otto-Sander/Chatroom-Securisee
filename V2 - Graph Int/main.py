"""
main.py
----------------------------------------------------------------------------------------------------------------
Ce fichier contient le point d'entrée principal pour l'application de Data Room Virtuelle. 
Il crée une instance de la classe LoginWindow et lance l'interface utilisateur graphique pour 
l'authentification de l'utilisateur.
----------------------------------------------------------------------------------------------------------------
Fonctionnalités :
- Initialisation de l'application.
- Affichage de la fenêtre de connexion en utilisant la classe LoginWindow.
"""
import tkinter as tk
from login_window import LoginWindow
from tkinter import *
from PIL import ImageTk, Image

#MainLoop
if __name__ == "__main__":
    #Fenêtre principale
    root = tk.Tk()
    root.state('zoomed')

    # Charger l'image et la redimensionner pour qu'elle s'adapte à la taille de la fenêtre
    image = Image.open("Images\Background_Welcomming_flou.png")
    image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    
    background_image = ImageTk.PhotoImage(image)
    label = Label(root,image=background_image)
    label.place(x=0,y=0,relwidth=1,relheight=1)

    #Lance l'application
    app = LoginWindow(root)
    root.mainloop()