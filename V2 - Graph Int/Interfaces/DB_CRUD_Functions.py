############################
# CREATE FUNCTIONS
############################

# Fonction qui créé une session (l'utilisateur doit être login)
def create_new_session(client, code, password, id_user1, id_user2, id_user3, id_user4, id_user5, id_user6, id_user7, id_user8, id_user9, id_user10):
    data = client.table("session").insert({"code": code, "password": password, "id_user1": id_user1, "id_user2": id_user2, "id_user3": id_user3, "id_user4": id_user4, "id_user5": id_user5, "id_user6": id_user6, "id_user7": id_user7, "id_user8": id_user8, "id_user9": id_user9, "id_user10": id_user10}).execute()

# Fonction qui créé un server
def create_new_server(client, ip, port):
    data = client.table("serveur").insert({"IP": ip, "port": port}).execute()

# Fonction qui créé une connexion (l'utilisateur doit être login)
def create_new_connection(client, user_id, channel_code, ip, port):
    try:
        data = client.table("connections").insert({"user_id": user_id, "channel_code": channel_code, "ip": ip, "port": port}).execute()
    except Exception as e:
        print(f"Error in create_new_connection: {e}")


###############################
# READ FUNCTIONS
###############################
def get_last_server(client):
    data = client.table("serveur").select("*").execute()
    return data.data[-1]["IP"], data.data[-1]["port"]

# Fonction récupère toutes les infos d'un serv
def get_server_all(client, id):
    data = client.table("serveur").select("*").eq("id", id).execute()
    return data.data

# Fonction qui retourne l'IP d'un serv
def get_server_IP(client, id):
    data = client.table("serveur").select("IP").eq("id", id).execute()
    return data.data[0]["IP"]

# Fonction qui retourne le port d'un serv
def get_server_port(client, id):
    data = client.table("serveur").select("port").eq("id", id).execute()
    return data.data[0]["port"]

# Fonction qui retourne toutes les infos d'une session
def get_session_all(client, session_code):
    try:
        response = client.table("session").select("*").eq("code", session_code).execute()
        print("response",response)
        if response and response.data:
            return response.data
        else:
            return []
    except Exception as e:
        print(f"Error in get_session_all: {e}")
        return []

# Fonction qui retourne l'id d'une session
def get_session_id(client, code):
    data = client.table("session").select("id").eq("code", code).execute()
    print('id_data:',data)
    return data.data[0]["id"]

# Fonction qui retourne le mot de passe d'une session
def get_session_password(client, code):
    data = client.table("session").select("password").eq("code", code).execute()
    return data.data[0]["password"]

# Fonction qui retourne l'id des utilisateurs d'une session
def get_session_users(client, session_code):
    try:
        response = get_session_all(client, session_code)
        if not response:
            print("No session found with the provided session code.")
            return []
        users = []
        session = response[0]
        for col in ['id_user1', 'id_user2', 'id_user3', 'id_user4', 'id_user5', 'id_user6', 'id_user7', 'id_user8', 'id_user9', 'id_user10']:
            user_id = session.get(col)
            if user_id:
                users.append(user_id)
        return users
    except Exception as e:
        print(f"Error in get_session_users: {e}")
        return []

# Fonction qui retourne toutes les infos d'une connection
def get_connection_all(client, user_id):
    data = client.table("connections").select("*").eq("user_id", user_id).execute()
    return data.data

# Fonction qui retourne l'id d'une connection
def get_connection_id(client, user_id):
    data = client.table("connections").select("connection_id").eq("user_id", user_id).execute()
    return data.data[0]["connection_id"]

# Fonction qui retourne le channel_code d'une session
def get_connection_channel_code(client, user_id):
    data = client.table("connections").select("channel_code").eq("user_id", user_id).execute()
    return data.data[0]["channel_code"]

# Fonction qui retourne l'ip d'une connection
def get_connection_ip(client, user_id):
    data = client.table("connections").select("ip").eq("user_id", user_id).execute()
    return data.data[0]["ip"]

# Fonction qui retourne le port d'une connection
def get_connection_port(client, user_id):
    data = client.table("connections").select("port").eq("user_id", user_id).execute()
    return data.data[0]["port"]


#############################
# UPDATE FUNCTIONS
#############################


# Fonction pour modifer la table session (l'utilisateur doit être log in)
def update_session_new_user(client, next_column, new_user, code):
    data = client.table("session").update({next_column: new_user}).eq("code", code).execute()

# Fonction qui ajoute un nouvel utilisateur dans la session
def add_next_user_in_session(client, session_code, new_user):
    try:
        # Récupérer la ligne avec l'ID spécifié
        response = get_session_all(client, session_code)

        if not response:
            print("No session found with the provided session code.")
            return

        session = response[0]

        # Déterminer la première colonne null
        next_column = None
        for col in ['id_user1', 'id_user2', 'id_user3', 'id_user4', 'id_user5', 'id_user6', 'id_user7', 'id_user8', 'id_user9', 'id_user10']:
            if session.get(col) is None:
                next_column = col
                break

        if next_column is None:
            print("All user columns are already filled.")
        else:
            # Mettre à jour la colonne avec le nouvel utilisateur
            update_session_new_user(client, next_column, new_user, session_code)
    except Exception as e:
        print(f"Error in add_next_user_in_session: {e}")


########################################
# DELETE FUNCTIONS
########################################

# Fonction qui supprime un server
def delete_server(client, ip):
    data = client.table("serveur").delete().eq("IP", ip).execute()

# Fonction qui supprime un utilisateur d'une session
def delete_user_in_session(client, session_code, id_user):
    response = get_session_all(client, session_code)

    if not response:
        print("No session found with the provided session code.")
        return

    session = response[0]  # Assumer que response est une liste

    column_to_find = None
    for col in ['id_user1', 'id_user2', 'id_user3', 'id_user4', 'id_user5', 'id_user6', 'id_user7', 'id_user8', 'id_user9', 'id_user10']:
        if session[col] == str(id_user):  # Convertir l'UUID en chaîne
            column_to_find = col
            break
    if column_to_find is None:
        print("User is not in session.")
    else:
        # Mettre à jour la colonne avec le nouvel utilisateur
        client.table("session").update({column_to_find: None}).eq("code", session_code).execute()



# Fonction qui supprime une session
def delete_session(client, session_code):
    data = client.table("session").delete().eq("code", session_code).execute()

# Fonction qui supprime une connection
def delete_connection(client, user_id):
    data = client.table("connections").delete().eq("user_id", user_id).execute()

