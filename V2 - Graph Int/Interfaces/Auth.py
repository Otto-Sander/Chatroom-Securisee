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
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        return True
    # Incorrect Passwd/Username/Email doesn't check
    except gotrue.errors.AuthApiError as e:
        return False

#Fonction qui déconnecte un utilisateur
def log_out_user(client):
    res = client.auth.sign_out()

# Fonction qui retourne l'id de l'utilisateur qui est connecté
def get_current_connected_user_id(client):
    data = client.auth.get_user()
    return data.user.id

# Fonction qui permet de retourner le username de l'utilisateur connecté
def get_current_connected_username(client):
    data = client.auth.get_user()
    return data.user_metadata.get('username')

# Fonction qui retourne le mail de l'utilisateur qui est connecté
def get_current_connected_user_email(client):
    data = client.auth.get_user()
    return data.user.email