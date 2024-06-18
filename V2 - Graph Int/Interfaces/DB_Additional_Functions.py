from DB_CRUD_Functions import *

#Fonction qui vérifie si un utilisateur existe dans la database
def is_user_in_database(client, username):
    data = get_user_all(client, username)
    if(data == []):
        print("This user is not in the dataBase !  :(")
    else:
        print("This user is in the dataBase !  :)")

#Fonction qui vérifie si une session existe dans la database
def is_session_in_database(client, code):
    data = get_session_all(client, code)
    if(data == []):
        print("This session is not in the dataBase !  :(")
    else:
        print("This session is in the dataBase !  :)")
