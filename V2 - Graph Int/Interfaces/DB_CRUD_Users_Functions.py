###############################
# READ FUNCTIONS
###############################

#Fonction pour récuper les infos de l'utilisateur authentifé
#Retourne un dictionnaire de toutes les infos de cet utilisateur
def get_user_all(client, mail):
    data = client.table("profile").select("*").eq("email", mail).execute()
    print("data:",data)
    return data.data

# Fonction qui retourne tous les mails de la table profil (user existant)
def get_user_all_mail(client):
    data = client.table("profile").select("email").execute()
    return data.data

#Fonction pour récupérer le mot de passe d'un utilisateur connecté
def get_password(client, mail):
    data = client.table("profile").select("password").eq("email", mail).execute()
    return data.data[0]["password"]


#Fonction pour récupérer le username d'un utilisateur connecté
def get_username(client, mail):
    data = client.table("profile").select("username").eq("email", mail).execute()
    return data.data[0]["username"]


# Fonction pour récupérer l'id d'un utilisateur
def get_id(client, mail):
    data = client.table("profile").select("id").eq("mail", mail).execute()
    return data.data[0]["id"]

# Fonction afin de récupérer l'id user à partir de l'ip
def get_id_by_ip(client,ip):
    data = client.table("connections").select("user_id").eq("ip",ip).execute()
    print("data_function:",data.data[0]["user_id"])
    return data.data[0]["user_id"]


#############################
# UPDATE FUNCTIONS
#############################

# Fonction pour modifier le mail d'un utilisateur authentifié (l'utilisateur doit être login)
def update_user_mail(client, newMail):
    data = client.auth.update_user({"email": newMail})


#Fonction pour modifier le mot de passe d'un utilisateur authentifié (l'utilisateur doit être log in)
def update_user_password(client, newPassword):
    data = client.auth.update_user({"password": newPassword})
 
#Fonction pour modifier le pseudo d'un utilisateur
def update_user_username(client, newUsername, email):
    data = client.table("profile").update({"username": newUsername}).eq("email", email).execute()