import gotrue.errors
from dotenv import load_dotenv
load_dotenv()

import os

from supabase import create_client

from DB_Additional_Functions import *
from Auth import *
from DB_CRUD_Functions import *
from DB_CRUD_Users_Functions import *


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

email: str = "nathan.simoes@efrei.net"
password: str = "rootrootroot"

#FONCTIONS DE TESTS
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

#add_new_user(supabase, email, password, "Natha80")

data = supabase.auth.sign_in_with_password({"email": email, "password": password})

print("Logged In !!")

#update_user_password(supabase, "rootroot")

print("Current user id : ")
print(get_current_connected_user_id(supabase))

print("Current user mail : ")
print(get_current_connected_user_email(supabase))

res = supabase.auth.sign_out()

print("Signed out ! ")