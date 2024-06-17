from CRUD_Functions import *

#Fonction qui vérifie si un utilisateur existe dans la database
def is_in_database(client, username):
    data = get_user_all(client, username)
    if(data == []):
        print("This user is not in the dataBase !  :(")
    else:
        print("This user is in the dataBase !  :)")
