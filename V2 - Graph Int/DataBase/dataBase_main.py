from dotenv import load_dotenv
load_dotenv()

import os

from supabase import create_client

from CRUD_Functions import *
from Additional_Functions import *

if __name__ == '__main__':
    #Créer le client
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)


    ##FONCTIONS DE TESTS
    #data = add_user(supabase, "Booo", "ROot", "nathan88@gmail.com")
    #data = add_session(supabase, 45687, "192.168.56.12", 53, "10.0.0.1", 45)
    #data = get_all_users(supabase)
    #data = get_user_all(supabase, "Boooo")
    #data = get_password(supabase, "Booo")
    #data = get_mail(supabase, "Booo")
    #print(data)

    #is_in_database(supabase, "Neith")