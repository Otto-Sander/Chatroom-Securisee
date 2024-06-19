
#############################
# CREATE FUNCTIONS
#############################

# Fonction pour ajouter un utilisateur
def add_user(client, Username, Pass, Mail):
    data = client.table("utilisateurs").insert({"username": Username, "password": Pass, "mail": Mail}).execute()
    return data

# Fonction pour ajouter une session
def add_session(client, Code, IP_Public, Port_SERV, IP_Privee, Port_Priv):
    data = client.table("sessions").insert({"code": Code, "IP_public": IP_Public, "Port_Server": Port_SERV, "IP_privee": IP_Privee, "Port_privee": Port_Priv}).execute()
    return data


###############################
# READ FUNCTIONS
###############################

# Fonction pour récupérer la liste de tous les utilisateurs
# Chaque éléments de la liste est un dictionnaire composé de toutes les infos de l'utilisateur en question
def get_all_users(client):
    data = client.table("utilisateurs").select("*").execute()
    return data.data

# Fonction pour récupérer les infos d'un utilisateur précisément
# Retourne un dictionnaire de toutes les infos de cet utilisateur
def get_user_all(client, username):
    data = client.table("utilisateurs").select("*").eq("username", username).execute()
    return data.data

# Fonction pour récupérer le mot de passe d'un utilisateur spécifique
def get_password(client, username):
    data = client.table("utilisateurs").select("password").eq("username", username).execute()
    return data.data[0]["password"]

# Fonction pour récupérer le mail d'un utilisateur spécifique
def get_mail(client, username):
    data = client.table("utilisateurs").select("mail").eq("username", username).execute()
    return data.data[0]["mail"]

#Fonction pour récupérer l'id d'un utilisateur
def get_id(client, username):
    data = client.table("utilisateurs").select("id").eq("username", username).execute()
    return data.data[0]["id"]

#Fonction pour récupérer la liste de toutes les sessions
#Chaque éléments de la liste est un dictionnaire composé de toutes les infos de la session en question
def get_all_sessions(client):
    data = client.table("sessions").select("*").execute()
    return data.data

#Fonction pou récupérer les infos d'une session précisément
#Retourne un dictionnaire de toutes les infos de cet utilisateur
def get_session_all(client, code):
    data = client.table("sessions").select("*").eq("code", code).execute()
    return data.data

#Fonction pour récupérer l'IP publique de la session
def get_IP_public(client, code):
    data = client.table("sessions").select("IP_public").eq("code", code).execute()
    return data.data[0]["IP_public"]

#Fonction pour récupérer le Port Server de la session
def get_Port_Server(client, code):
    data = client.table("sessions").select("Port_Server").eq("code", code).execute()
    return data.data[0]["Port_Server"]

#Fonction pour récupérer l'IP privée de la session
def get_IP_privee(client, code):
    data = client.table("sessions").select("IP_privee").eq("code", code).execute()
    return data.data[0]["IP_privee"]

#Fonction pour récupérer l'IP privée de la session
def get_Port_privee(client, code):
    data = client.table("sessions").select("Port_privee").eq("code", code).execute()
    return data.data[0]["Port_privee"]



################################
# UPDATE FUNCTIONS
################################


# Fonction pour modifier les infos d'un utilisateur
def update_user(client, username, new_username, password, mail):
    data = client.table("utilisateurs").update({"username": new_username, "password": password, "mail": mail}).eq("username", username).execute()

# Fonction pour modifier l'username d'un utilisateur
def update_username(client, username, new_username):
    data = client.table("utilisateurs").update({"username": new_username}).eq("username", username).execute()

# Fonction pour modifier le mot de passe d'un utilisateur
def update_password(client, username, new_password):
    data = client.table("utilisateurs").update({"password": new_password}).eq("username", username).execute()

# Fonction pour modifier le mail d'un utilisateur
def update_mail(client, username, new_mail):
    data = client.table("utilisateurs").update({"mail": new_mail}).eq("username", username).execute()


###########################################
# DELETE FUNCTIONS
###########################################

# Fonction qui supprime un utilisateur
def delete_user(client, username):
    data = client.table("utilisateurs").delete().eq("username", username).execute()

# Fonction qui supprime une session
def delete_session(client, code):
    data = client.table("sessions").delete().eq("code", code).execute()