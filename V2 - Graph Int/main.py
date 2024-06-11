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

#MainLoop
if __name__ == "__main__":
    #Fenêtre principale
    root = tk.Tk()
    root.state('zoomed')
    root.configure(background=
                   #'#152242'
                   'white'
                   )
    #Lance l'application
    app = LoginWindow(root)
    root.mainloop()