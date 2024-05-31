from taipy.gui import notify
from model.user import User
import re
import datetime

signed_in = False
user_id = ""
signin_date = None

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def on_signin_finish(state, id, payload):
    id = payload["args"][0]

    if id == 0:
        do_signin(state)
    else:
        state.show_signin_dialog = False
    return

def do_signin(state):
    if not is_valid_email(state.email):
        notify(state, "W", "Please enter a valid email address.")
        return
    
    if state.password == "":
        notify(state, "W", "Please enter your password.")
        return
    
    user = User(state.email, state.password)
    res = User.sign_in(user)
    
    if res == None:
        notify(state, "W", "Email address not found. Please sign up for an account.")
        return
    
    elif res == False:
        notify(state, "W", "Incorrect password. Please try again.")
        return
    
    else:
        state.user_id = res
        state.signed_in = True
        notify(state, "S", "Welcome back to ByteTalented, You have successfully signed in.")
        state.show_signin_dialog = False
        state.signin_date = datetime.datetime.now()
        return
    return