from dotenv import load_dotenv
load_dotenv()

import os

from supabase import create_client

from DB_Additional_Functions import *


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
    #data = get_id(supabase,"Neith")
    #print(data)

    #data = update_user(supabase, "Booo", "Boubou", "TEst", "pop@gmail.com")
    #data = update_username(supabase, "Neith", "Neith12")
    #data = update_password(supabase, "Neith12", "AAAHH15")

    #data = delete_user(supabase, "Neith12")
    #data = delete_session(supabase, 45687)

    #is_user_in_database(supabase, "Neith")
    #is_session_in_database(supabase, 45687)