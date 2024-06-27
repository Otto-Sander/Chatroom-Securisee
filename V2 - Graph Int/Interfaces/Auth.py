#################################
#AUTH FUNCTIONS
#################################
import gotrue.errors


#Fonction qui créé un nouvel utilisateur
def add_new_user(client, email, password):

    #Ajout d'un nouvel utilisateur dans la table auth.users
    newUser = client.auth.sign_up({"email": email, "password": password})


#Fonction qui connecte un utilisateur en vérifiant s'il a bien confirmé son email
def log_in_user(client, email, password):
    confirm = False
    while(confirm == False):
        ans = input("Did you confirm your email ? (type 'no' if you didn't) : ")
        while(ans == "no"):
            print("You need to confirm your email.")
            ans = input("Did you confirm your email ? : ")
        try:
            res = client.auth.sign_in_with_password({"email": email, "password": password})
            confirm = True
        except gotrue.errors.AuthApiError:
            print("You did not confirm your email, confirm it.")
            confirm = False

#Fonction qui déconnecte un utilisateur
def log_out_user(client):
    res = client.auth.sign_out()

# Fonction qui retourne l'id de l'utilisateur qui est connecté
def get_current_connected_user_id(client):
    data = client.auth.get_user()
    return data.user.id

# Fonction qui retourne le mail de l'utilisateur qui est connecté
def get_current_connected_user_email(client):
    data = client.auth.get_user()
    return data.user.email