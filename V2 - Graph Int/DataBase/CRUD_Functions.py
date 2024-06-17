
#############################
# Create Functions
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
# Read Functions
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