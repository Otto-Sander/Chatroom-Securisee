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
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
import tkinter as tk
from main_interface import MainInterface
from tkinter import *
from PIL import ImageTk, Image


#MainLoop
if __name__ == "__main__":
    #Fenêtre principale
    root = tk.Tk()

    #getting screen width and height of display
    width= root.winfo_screenwidth()
    height= root.winfo_screenheight()
    print("Width :",width,"Height:",height)

    #setting tkinter window size
    root.geometry(f"{width}x{height}")

    # Background
    image = Image.open("Images/background.jpg")
    image = image.resize((width, height))

    background_image = ImageTk.PhotoImage(image)
    label = Label(root,image=background_image)
    label.place(x=0,y=0,relwidth=1,relheight=1)
    #Lance l'application
    app = MainInterface(root)
    root.mainloop()